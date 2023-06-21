import os, json, pygame

def load_existing_save(savefile):
    with open(os.path.join(savefile), 'r+') as file:
        controls = json.load(file)
    return controls

def write_save(data):
    with open(os.path.join(os.getcwd(), 'save.json'), 'w') as file:
        json.dump(data, file)

def load_save():
    try:
        #Save is loaded
        save = load_existing_save('save.json')
    except:
        #No save file, so create a new one
        save = create_save()
        write_save(save)
    return save
def create_save():
    new_save = {
        "controls":{
            "0" :{"Col1": pygame.K_a, "Col2": pygame.K_s, "Col3": pygame.K_d, 
                  "Col4": pygame.K_j, "Col5": pygame.K_k, "Col6": pygame.K_l,
                  "Up": pygame.K_UP, "Down": pygame.K_DOWN, "Action1": pygame.K_SPACE} 
        },
        "current_profile": 0
    }

    return new_save

def reset_keys(actions):
    for action in actions:
        actions[action] = False
    return actions