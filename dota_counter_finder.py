import most_picked_heroes
import counter_heroes
import sys
from prettytable import PrettyTable
import asyncio

async def main(role, hero_name):
    print(f"Best {role} counters for {hero_name}:")
    position_heroes_names = most_picked_heroes.get_position_heroes_names(role)
    counter_heroes_list = await counter_heroes.get_counter_heroes(hero_name)
    table = PrettyTable(['hero name', 'disadvantage', f'{hero_name} win rate', 'matches played'])
    for counter_hero in counter_heroes_list:
        if(counter_hero.name.lower() in position_heroes_names and counter_hero.disadvantage > 0.5):
            table.add_row([counter_hero.name, f"{round(counter_hero.disadvantage,2)}%", f"{round(counter_hero.win_rate,2)}%", counter_hero.matches_played])
    print(table)
if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2]))