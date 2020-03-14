
def trivial_behavior(state):
    return True

def playing_reset(state):
    state["petMeters"]["ready_to_play"] = 0
    return True

def call_owner(state):
    print("Cat is crying in front of the empty food bowl.")
    return False

def eat(state):
    state["petItems"]["food_bowl"] += 5
    if state["petItems"]["food_bowl"] > 100:
        state["petItems"]["food_bowl"] = 100
    state["petMeters"]["hunger"] -= 20
    if state["petMeters"]["hunger"] < 0:
        state["petMeters"]["hunger"] = 0
    print("Cat is eating food from the food bowl.")
    return True

def meow(state):
    state["petMeters"]["social"] -= 40
    if state["petMeters"]["social"] < 0:
        state["petMeters"]["social"] = 0
    print("Cat is meowing to you.")
    return True

def ready_to_play(state):
    state["petMeters"]["ready_to_play"] = 1
    return True

def play_alone(state):
    state["petMeters"]["fun"] -= 30
    if state["petMeters"]["fun"] < 0:
        state["petMeters"]["fun"] = 0
    state["petMeters"]["energy"] += 15
    if state["petMeters"]["energy"] > 100:
        state["petMeters"]["energy"] = 100
    print("Cat is meowing to you.")
    return True

def box_relief(state):
    state["petMeters"]["bladder"] = 0
    state["petItems"]["litter_box"] += 30
    if state["petItems"]["litter_box"] > 100:
        state["petItems"]["litter_box"] = 100
    print("Cat is reliefing in the litter box.")
    return True

def improper_relief(state):
    state["petMeters"]["bladder"] = 0
    state["petItems"]["shit_on_floor"] += 1
    print("Cat is reliefing on the floor.")
    return True
	
def clean_self(state):
    state["petMeters"]["hygiene"] -= 25
    if state["petMeters"]["hygiene"] < 0:
        state["petMeters"]["hygiene"] = 0
    print("Cat is licking itself.")
    return True

def go_to_sleep(state):
    state["petMeters"]["sleeping"] = 1
    print("Cat is falling asleep.")
    return True

def sleeping(state):
    state["petMeters"]["energy"] -= 20
    if state["petMeters"]["energy"] < 0:
        state["petMeters"]["energy"] = 0
    print("Cat is sleeping.")
    return True
