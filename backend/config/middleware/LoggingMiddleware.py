from datetime import datetime
import pytz
import time
import logging
import json
import traceback

request_logger = logging.getLogger("middleware")
exception_logger = logging.getLogger("exception")


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.cached_request_body = None
        self.response_limit = 500

    def __call__(self, request):
        self.cached_request_body = request.body
        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    def get_client_ip_address(self, request):
        req_headers = request.META
        x_forwarded_for_value = req_headers.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for_value:
            ip_addr = x_forwarded_for_value.split(",")[-1].strip()
        else:
            ip_addr = req_headers.get("REMOTE_ADDR")
        return ip_addr

    """http 요청 미들웨어"""

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        try:
            seoul_tz = pytz.timezone("Asia/Seoul")
            seoul_time = datetime.now(seoul_tz)

            log_data = {
                "DATE": str(seoul_time),
                "REMODE_ADDR": self.get_client_ip_address(request)
                if "REMOTE_ADDR" in request.META.keys()
                else None,
                "PATH_INFO": request.get_full_path(),
                "STATUS_CODE": response.status_code,
                "METHOD": request.method,
                "QUERY_STRING": request.META["QUERY_STRING"]
                if "QUERY_STRING" in request.META.keys()
                else None,
                "USER_ID": request.user.uuid
                if str(request.user) != "AnonymousUser"
                else None,
                "USER_NAME": request.user.username
                if str(request.user) != "AnonymousUser"
                else None,
                "RESPONSE_TIME": round(time.time() - request.start_time, 8),
                "HTTP_USER_AGENT": request.META["HTTP_USER_AGENT"]
                if "HTTP_USER_AGENT" in request.META.keys()
                else None,
                "LEVEL": "INFO",
            }

            try:
                log_data["BODY"] = (
                    json.loads(self.cached_request_body)
                    if self.cached_request_body
                    else None
                )
            except Exception as e:
                log_data["BODY"] = (
                    str(self.cached_request_body) if self.cached_request_body else None
                )

            if (
                log_data["HTTP_USER_AGENT"]
                and "ELB-HealthChecker" in log_data["HTTP_USER_AGENT"]
            ):
                return response

            if response.content:
                log_data["RESPONSE"] = (
                    str(json.loads(response.content))[: self.response_limit]
                    if getattr(response, "content")
                    else None
                )

            # 민감한 정보제거.
            if "token" in log_data["PATH_INFO"]:
                log_data["BODY"] = None
                log_data["RESPONSE"] = None

            if response.status_code in range(400, 500):
                log_data["LEVEL"] = "ERROR"
                exception_logger.error(log_data)
            elif response.status_code in range(500, 600):
                log_data["LEVEL"] = "CRITICAL"
                exception_logger.error(log_data)

            request_logger.info(log_data)

        except Exception as e:
            print(f"[LOGGING ERROR]", e)
            print(traceback.format_exc())
            print(request.method, request.get_full_path())

        return response
