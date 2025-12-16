from bs4 import BeautifulSoup
import zendriver as zd

class CounterHero:
    def __init__(self, name, disadvantage, win_rate, matches_played):
        self.name = name
        self.disadvantage = disadvantage
        self.win_rate = win_rate
        self.matches_played = matches_played

async def get_counter_heroes(hero_name):
    browser = await zd.start()
    counter_heroes = []

    try:
        hero_name = hero_name.lower().replace(' ', '-')
        url = f"https://www.dotabuff.com/heroes/{hero_name}/counters?date=patch_7.40"
        
        print(f"Fetching data for {hero_name}...")
        page = await browser.get(url)

        await page.wait(2)
        
        soup = BeautifulSoup(await page.get_content(), 'html.parser')

        table = soup.find('table', class_='sortable')
        if not table:
            print("Error: Could not find the data table (Check hero name).")
            return []

        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) >= 4:
                name = cols[1].text.strip()
                
                try:
                    disadv = float(cols[2].get('data-value', 0))
                    win_rt = float(cols[3].get('data-value', 0))
                    matches = int(cols[4].get('data-value', 0).replace(',', ''))
                    
                    counter_heroes.append(CounterHero(name, disadv, win_rt, matches))
                except ValueError:
                    continue

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await browser.stop()
        
    return counter_heroes