
def trivial_behavior(state):
    return True

def playing_reset(state):
    state["petMeters"]["ready_to_play"] = False
    return True

def call_owner(state):
    print("{} is looking at the empty food bowl.".format(state["petName"]))
    return False

def eat(state):
    state["petItems"]["food_bowl"] -= 5
    if state["petItems"]["food_bowl"] < 0:
        state["petItems"]["food_bowl"] = 0
    state["petMeters"]["hunger"] -= 20
    if state["petMeters"]["hunger"] < 0:
        state["petMeters"]["hunger"] = 0
    print("{} is eating food from the food bowl.".format(state["petName"]))
    return True

def fish_eat(state):
    state["petItems"]["food_in_tank"] -= 1
    print("{} is eating some fish food.".format(state["petName"]))
    return True

def meow(state):
    state["petMeters"]["social"] -= 5
    if state["petMeters"]["social"] < 0:
        state["petMeters"]["social"] = 0
    print("{} is meowing to you.".format(state["petName"]))
    return True

def ready_to_play(state):
    state["petMeters"]["ready_to_play"] = True
    return True

def play_alone(state):
    state["petMeters"]["fun"] -= 30
    if state["petMeters"]["fun"] < 0:
        state["petMeters"]["fun"] = 0
    state["petMeters"]["energy"] += 15
    if state["petMeters"]["energy"] > 100:
        state["petMeters"]["energy"] = 100
    print("{} is playing with a toy.".format(state["petName"]))
    return True

def box_relief(state):
    state["petMeters"]["bladder"] = 0
    state["petItems"]["litter_box"] -= 30
    if state["petItems"]["litter_box"] < 0:
        state["petItems"]["litter_box"] = 0
    print("{} is relieving in the litter box.".format(state["petName"]))
    return True

def improper_relief(state):
    state["petMeters"]["bladder"] = 0
    state["petItems"]["shit_on_floor"] = True
    print("{} is relieving on the floor.".format(state["petName"]))
    return True

def clean_self(state):
    state["petMeters"]["hygiene"] -= 25
    if state["petMeters"]["hygiene"] < 0:
        state["petMeters"]["hygiene"] = 0
    print("{} is licking itself.".format(state["petName"]))
    return True

def go_to_sleep(state):
    state["petMeters"]["sleeping"] = True
    print("{} is falling asleep.".format(state["petName"]))
    return True

def sleeping(state):
    state["petMeters"]["energy"] -= 20
    if state["petMeters"]["energy"] < 0:
        state["petMeters"]["energy"] = 0
    print("{} is sleeping.".format(state["petName"]))
    return True

def dog_shaking(state):
    print("{} is feeling uncomfortable and shaking their body.".format(state["petName"]))
    return False

def bark_for_food(state):
    print("{} is barking in front of the food bowl.".format(state["petName"]))
    return False

def bark_at_door(state):
    print("{} is barking at the door.".format(state["petName"]))
    return True

def dog_proper_relief(state):
    print("{} is relieving in the back yard.".format(state["petName"]))
    state["petMeters"]["bladder"] = 0
    return True

def running_around(state):
    print("{} is running around the house.".format(state["petName"]))
    state["petMeters"]["fun"] -= 20
    if state["petMeters"]["fun"] < 0:
        state["petMeters"]["fun"] = 0
    state["petMeters"]["energy"] += 15
    if state["petMeters"]["energy"] > 100:
        state["petMeters"]["energy"] = 100

def barking(state):
    state["petMeters"]["social"] -= 40
    if state["petMeters"]["social"] < 0:
        state["petMeters"]["social"] = 0
    print("{} is barking at you.".format(state["petName"]))

def swim(state):
    print("{} is swimming around and seems to be doing alright.".format(state["petName"]))
    return True

def swim_slowly(state):
    print("{} is swimming more slowly than usual and seems to be out of energy.".format(state["petName"]))
    return True

def swim_sideways(state):
    print("{} is swimming sideways in the tank.".format(state["petName"]))
    return True
