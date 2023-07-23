from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point

from api.common.models import LogModel
from api.v1.model_history.models import ModelTracker

from random import randrange


class CulturePlace(ModelTracker):
    name = models.CharField("극장이름", max_length=64)
    address = gis_models.CharField(
        "주소", max_length=256, blank=True, null=False, default="알 수 없음"
    )
    latitude = gis_models.FloatField(
        "위도", blank=True, null=False, default=randrange(-100, -1) / 100
    )
    longitude = gis_models.FloatField(
        "경도", blank=True, null=False, default=randrange(-100, -1) / 100
    )
    coord = gis_models.PointField(
        "좌표", srid=4326, spatial_index=True, null=False, default=Point(0, 0, srid=4326)
    )

    class Meta:
        db_table = "culture_place"
        verbose_name_plural = "관람 장소"


class Culture(ModelTracker, LogModel):
    class CultureType(models.IntegerChoices):
        UNKNOW = (0, "미정")
        MUSICAL = (1, "뮤지컬")
        CONCERT = (2, "콘서트")
        DRAMA = (3, "연극")
        CLASSIC = (4, "클래식")

    culture_type = models.IntegerField(
        "문화종류",
        choices=CultureType.choices,
        default=CultureType.UNKNOW,
        blank=True,
        null=True,
    )

    title = models.CharField("제목", max_length=128, blank=True, null=False)
    place = models.ForeignKey(
        CulturePlace,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="place",
        verbose_name="관람장소",
    )
    period_from = models.DateField("시작일", blank=True, null=False)
    period_to = models.DateField("시작일", blank=True, null=False)

    class Meta:
        db_table = "culture"
        verbose_name = "문화정보"
