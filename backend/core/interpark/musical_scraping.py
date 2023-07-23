import requests
from bs4 import BeautifulSoup
import re
 
class MusicalScrapper:

    def __init__(self) -> None:
        self.url = 'http://ticket.interpark.com/TPGoodsList.asp?Ca=Mus'
    
    def __get_html(self):
        response = requests.get(self.url)
 
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            return soup
        else: 
            print(response.status_code)
            return False
    
    def get_musical_list(self):
        soup = self.__get_html()

        musical_list = []

        if soup:
            # html에서 dl 태그 중 class이름이 info_spec인 태그를 찾아라
            wrapper = soup.find('div','Rk_gen2')

            list_table = wrapper.find('table')
            list_table = list_table.find_all("tr")
            for content in list_table:
                td_list = content.find_all("td")
                if td_list:
                    title = td_list[1].find("a").text
                    place = td_list[2].find("a").text
                    period = td_list[3].text

                    pattern = r"\s+"
                    period = re.sub(pattern, "", period)

                    musical_list.append({
                        "title": title,
                        "place": place,
                        "period": period
                    })
        
        return musical_list