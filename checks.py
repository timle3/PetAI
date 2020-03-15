
def trivial_check(state):
    return True

def if_bowl_full(state):
    return state["petItems"]["food_bowl"] > 0

def social_meter(state):
    return state["petMeters"]["social"] > 35

def check_box(state):
    return state["petItems"]["litter_box"] > 0

# For dogs/cats, are they feeling dirty?
# For the fish, is the tank clean?
def pet_feeling_clean():
    return state["petMeters"]["hygiene"] > 50
