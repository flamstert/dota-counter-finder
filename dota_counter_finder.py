import most_picked_heroes
import counter_heroes
import sys
from prettytable import PrettyTable


def main(hero_name, role):
    print(f"Best {role} counters for {hero_name}:")
    most_picked_heroes_list = most_picked_heroes.get_heroes_data(role)
    counter_heroes_list = counter_heroes.get_counter_heroes_names(hero_name)
    table = PrettyTable(['Hero Name', 'Disadvantage', 'Counter\'s Win Rate', 'Matches Played'])
    for counter_hero in counter_heroes_list:
        if(counter_hero.name in [hero.name for hero in most_picked_heroes_list] and counter_hero.disadvantage > 50):
            table.add_row([counter_hero.name, f"{counter_hero.disadvantage/100}%", f"{100-counter_hero.win_rate/100}%", counter_hero.matches_played])
    print(table)
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])