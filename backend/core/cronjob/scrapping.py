from core.interpark.musical_scraping import MusicalScrapper
from api.v1.culture.models import Culture


def interpark_musical_scrapper():
    musical_scrapper = MusicalScrapper()
    musical_list = musical_scrapper.get_musical_list()

    for musical in musical_list:
        title = musical["title"]
        place = musical["place"]
        period_from, period_to = musical["period"].split("~")
        period_from = period_from.replace(".", "-")
        period_to = period_to.replace(".", "-")

        try:
            culture = Culture.objects.get(
                title=title, period_from=period_from, period_to=period_to
            )
        except:
            culture = Culture.objects.create(
                title=title, period_from=period_from, period_to=period_to
            )
            culture.save()
