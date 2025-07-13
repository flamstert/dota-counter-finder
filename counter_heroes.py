from bs4 import BeautifulSoup
import requests

class CounterHero:
    def __init__(self, name, disadvantage, win_rate, matches_played):
        self.name = name
        self.disadvantage = disadvantage
        self.win_rate = win_rate
        self.matches_played = matches_played

    def __str__(self):
        return f"{self.name.ljust(20)} - Disadvantage: {str(f'{self.disadvantage/100}%').ljust(10)} {self.name} Win Rate: {str(f'{100-self.win_rate/100}%').ljust(20)} Matches Played: {self.matches_played}"

def get_counter_heroes_names(hero_name):
    hero_name = hero_name.lower().replace(' ', '-')
    url = f"https://www.dotabuff.com/heroes/{hero_name}/counters"
    user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    response = requests.get(url, headers=user_agent)
    soup = BeautifulSoup(response.content, 'html.parser')

    counter_heroes = []
    table = soup.find('table', class_='sortable')
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if len(cols) >= 4:
            hero_name = cols[1].text.strip()
            disadvantage = int(cols[2].text.replace('%', '').replace('.', ''))
            win_rate = int(cols[3].text.replace('%', '').replace('.', ''))
            matches_played = int(cols[4].text.replace(',', ''))
            counter_heroes.append(CounterHero(hero_name, disadvantage, win_rate, matches_played))

    return counter_heroes