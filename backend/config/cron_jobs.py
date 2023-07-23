from config.settings.base import BASE_DIR
import os

CRONJOBS = [
    (
        "0 1 * * *",
        "core.cronjob.scrapping.interpark_musical_scrapper",
        ">> " + os.path.join(BASE_DIR, "log/cron.log") + " 2>&1 ",
    ),
]


"""
1. apt-get install cron 이 설치되어야 함
2. service cron start # cron 서비스가 실행중이어야 django-crontab도 실행이 됨.
 -> service cron status 로 실행여부 확인

python manage.py crontab add
python manage.py crontab show
python manage.py crontab remove
"""
