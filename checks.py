
def trivial_check(state):
    return True

def if_bowl_full(state):
    return state["petItems"]["food_bowl"] > 0

def social_meter(state):
    return state["petMeters"]["social"] > 35

def check_box(state):
    return state["petItems"]["litter_box"] > 0
