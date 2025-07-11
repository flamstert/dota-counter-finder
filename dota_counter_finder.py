import most_picked_heroes
import counter_heroes
import sys

def main(hero_name, role):
    print(f"Best {role} counters for {hero_name}:")
    most_picked_heroes_list = most_picked_heroes.get_heroes_data(role)
    counter_heroes_list = counter_heroes.get_counter_heroes_names(hero_name)
    for counter_hero in counter_heroes_list:
        if(counter_hero.name in [hero.name for hero in most_picked_heroes_list] and counter_hero.disadvantage > 0):
            print(counter_hero)
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])