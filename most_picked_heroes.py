from bs4 import BeautifulSoup
import requests

class Hero:
    def __init__(self, name, win_rate, pick_rate):
        self.name = name
        self.win_rate = win_rate
        self.pick_rate = pick_rate

    def __str__(self):
        return f"{self.name} - Win Rate: {self.win_rate/100}%, Pick Rate: {self.pick_rate/100}%"

def get_role_name_encoded(name):
    match name.lower():
        case 'safe':
            return 'core-safe'
        case 'mid':
            return 'core-mid'
        case 'offlane':
            return 'core-off'
        case 'support':
            return 'support-off'
        case 'hard support':
            return 'support-safe'
        case _:
            return name

user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
def get_heroes_data(role):
    url = f"https://www.dotabuff.com/heroes?show=heroes&view=winning&mode=all-pick&date=7.39&rankTier=guardian&position={get_role_name_encoded(role)}"

    response = requests.get(url, headers=user_agent)
    soup = BeautifulSoup(response.content, 'html.parser')

    page = soup.find_all(class_='tw-border-b tw-transition-colors hover:tw-bg-muted/50 data-[state=selected]:tw-bg-muted')
    heroes = []
    for hero in page[1:]:
        hero_name = hero.contents[0].text
        hero_win_rate = int(hero.contents[1].text.replace('%', '').replace('.', ''))
        hero_pick_rate = int(hero.contents[2].text.replace('%', '').replace('.', ''))
        heroes.append(Hero(hero_name, hero_win_rate, hero_pick_rate))
    
    heroes.sort(key=lambda x: x.pick_rate, reverse=True)
    return heroes[:20]