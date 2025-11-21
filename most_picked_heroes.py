def get_role_name_encoded(name):
    match name.lower():
        case 'safe' | 'carry' | 'core':
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
            print(f"Unknown role: {name}")
            print("Please enter a valid role: safe, mid, offlane, support, hard support.")
            exit()
            return name

def get_position_heroes_names(role):
    with open(f'most-picked-heroes/{get_role_name_encoded(role)}.txt') as f:
        return f.readline().split(';')