def get_role_name_encoded(name):
    match name.lower():
        case 'safe' | 'carry' | 'core' | 'pos1':
            return 'core-safe'
        case 'mid' | 'middle' | 'pos2':
            return 'core-mid'
        case 'offlane' | 'off' | 'pos3':
            return 'core-off'
        case 'support' | 'soft' | 'pos4':
            return 'support-off'
        case 'hard support' | 'hard' | 'pos5':
            return 'support-safe'
        case _:
            print(f"Unknown role: {name}")
            print("Please enter a valid role: safe, mid, offlane, support, hard support.")
            exit()
            return name

def get_position_heroes_names(role):
    with open(f'most-picked-heroes/{get_role_name_encoded(role)}.txt') as f:
        return f.readline().split(';')