from django.db import models
from django.contrib.postgres.fields import ArrayField

from api.common.models import LogModel
from api.v1.model_history.models import ModelTracker
from api.v1.culture.models import Culture


class Job(models.Model):
    name = models.CharField("직업", max_length=16, blank=True, null=False)


class Actor(ModelTracker, LogModel):
    class Sex(models.IntegerChoices):
        UNKNOW = (0, "미정")
        MALE = (1, "남성")
        FEMALE = (2, "여성")

    name = models.CharField("이름", max_length=16, blank=True, null=False)
    other_name = ArrayField(
        models.CharField("다른이름", max_length=16), blank=True, null=True
    )
    jobs = models.ManyToManyField(
        Job,
        blank=True,
        related_name="job",
        verbose_name="직업",
    )

    birth = models.DateField("생년월일", blank=True, null=False)
    sex = models.IntegerField(
        "성별",
        choices=Sex.choices,
        default=Sex.UNKNOW,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "actor"
        verbose_name = "배우"


class ActorActivity(ModelTracker, LogModel):
    actor = models.ForeignKey(
        Actor,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="actor",
        verbose_name="배우활동",
    )

    culture = models.ForeignKey(
        Culture,
        on_delete=models.SET_NULL,
        default=None,
        blank=True,
        null=True,
        related_name="culture",
        verbose_name="출연작품",
    )

    character_name = models.CharField("캐릭터 이름", max_length=16, blank=True, null=False)
    character_birth = models.DateField("캐릭터 생년월일", blank=True, null=False)
    character_job = models.CharField("캐릭터 직업", max_length=16, blank=True, null=False)

    class Meta:
        db_table = "actor_activity"
        verbose_name = "배우"
        unique_together = [["actor", "culture"]]


class Company(ModelTracker, LogModel):
    name = models.CharField("기획사이름", max_length=32, blank=True, null=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "company"
        verbose_name = "기획사"


class ActorCompanyRelation(models.Model):
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        verbose_name="배우활동",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        verbose_name="배우활동",
    )
    start_date = models.DateField(blank=True, null=False)
    end_date = models.DateField(blank=True, null=False)

    def __str__(self):
        return f"{self.actor} - {self.company} ({self.start_date} ~ {self.end_date})"

    class Meta:
        db_table = "actor_company_relation"
        verbose_name = "배우 기획사 이력"
        unique_together = [["actor", "company", "start_date", "end_date"]]
