from dataclasses import dataclass
from bs4 import BeautifulSoup
import zendriver as zd
import asyncio
from typing import List
import json
import time
import os


@dataclass
class CounterHero:
    name: str
    disadvantage: float
    win_rate: float
    matches_played: int

def _parse_table_soup(soup: BeautifulSoup) -> List[CounterHero]:
    table_rows = soup.select('table.sortable tr')
    if not table_rows or len(table_rows) <= 1:
        return []

    counters = []
    for row in table_rows[1:]:
        cols = row.find_all('td')
        # Expect at least 5 columns: index, hero, disadvantage, winrate, matches
        if len(cols) < 5:
            continue
        name = cols[1].get_text(strip=True)
        try:
            disadv = float(cols[2].get('data-value', '0'))
            win_rt = float(cols[3].get('data-value', '0'))
            matches = int(cols[4].get('data-value', '0').replace(',', ''))
        except (ValueError, AttributeError):
            continue
        counters.append(CounterHero(name, disadv, win_rt, matches))
    return counters


_CACHE_FILE = os.path.join(os.path.dirname(__file__), '.counter_cache.json')
_CACHE_TTL = 168 * 3600


def _load_cache():
    try:
        if not os.path.exists(_CACHE_FILE):
            return {}
        with open(_CACHE_FILE, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except Exception:
        return {}


def _save_cache(cache_data):
    try:
        with open(_CACHE_FILE, 'w', encoding='utf-8') as fh:
            json.dump(cache_data, fh)
    except Exception:
        pass


def _get_cached(hero_name: str):
    cache = _load_cache()
    entry = cache.get(hero_name)
    if not entry:
        return None
    if time.time() - entry.get('ts', 0) > _CACHE_TTL:
        # stale
        return None
    # reconstruct CounterHero objects
    return [CounterHero(**c) for c in entry.get('data', [])]


def _set_cache(hero_name: str, counters: List[CounterHero]):
    cache = _load_cache()
    cache[hero_name] = {
        'ts': time.time(),
        'data': [c.__dict__ for c in counters]
    }
    _save_cache(cache)


async def get_counter_heroes(hero_name: str):
    """Fetch counters using the browser and cache results."""
    hero_name = hero_name.lower().replace(' ', '-')

    # check persistent cache first
    cached = _get_cached(hero_name)
    if cached is not None:
        return cached

    browser = await zd.start()
    try:
        url = f"https://www.dotabuff.com/heroes/{hero_name}/counters?date=patch_7.40"

        print(f"Fetching data for {hero_name} via browser...")
        page = await browser.get(url)

        # Prefer waiting for the sortable table to appear if supported
        try:
            await page.wait_for_selector('table.sortable')
        except Exception:
            await page.wait(1)

        soup = BeautifulSoup(await page.get_content(), 'html.parser')
        counters = _parse_table_soup(soup)
        try:
            _set_cache(hero_name, counters)
        except Exception:
            pass
        return counters
    except Exception as e:
        print(f"An error occurred fetching data for {hero_name}: {e}")
        return []
    finally:
        await browser.stop()