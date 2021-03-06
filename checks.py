def trivial_check(state):
    return True

def if_bowl_full(state):
    return state["petItems"]["food_bowl"] > 0

def social_meter(state):
    return state["petMeters"]["social"] > 35

def check_box(state):
    return state["petItems"]["litter_box"] > 0

def dog_check_hygiene(state):
    return state["petMeters"]["hygiene"] > 70

def check_door(state):
    return state["petItems"]["door_opened"]

def check_bladder(state):
	return state["petMeters"]["bladder"] in range(90, 100)

def check_sleep(state):
    return state["petMeters"]["sleeping"]

# For the fish, is the tank clean?
def pet_feeling_clean(state):
    return state["petMeters"]["hygiene"] > 50

def food_in_tank(state):
    return state["petItems"]["food_in_tank"] > 0

def if_tank_clean(state):
    return state["petItems"]["tank_cleanliness"] > 10

def is_tired(state):
    return state["petMeters"]["energy"] > 70

def is_hungry(state):
    return state["petMeters"]["hunger"] > 50 
