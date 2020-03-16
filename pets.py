from bt_nodes import *
from checks import *
from behaviors import *
import random
import sys, os

# Disable printing to console
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore printing to console
def enablePrint():
    sys.stdout = sys.__stdout__

class Pet:
    def __init__(self, name=None):
        self.name = name

    def execute(self, state):
        raise NotImplementedError

class Dog(Pet):
    def __init__(self, name=None):
        self.name = name
        self.meter = {
            "hunger": 0,
            "energy": 0,
            "bladder": 0,
            "fun": 0,
            "hygiene": 0,
            "social": 0,
            "sleeping": False,
        }
        self.item = {
            "food_bowl": 0,
            "door_opened": False,
            "shit_on_floor": False
        }

    # Available actions for the owner (player) to do
    def actions(self, state, bt):
        print("Available Actions")
        print("1. Fill food bowl")
        if state["petItems"]["door_opened"] == True:
            print("2. Close the door")
        else:
            print("2. Open the door")
        if not state["petMeters"]["sleeping"]:
            print("3. Play with dog")
        print("4. Do nothing")
        print("5. Sleep")
        print("6. Check items")
        print("7. Clean mess")
        print("8. Give a bath")
        print()
        try:
            choice = int(input("Enter the number of the action you want to do: "))
            print()
            if choice == 1:
                state["petItems"]["food_bowl"] = 100
                print("Food bowl has been filled.")
            elif choice == 2:
                if state["petItems"]["door_opened"]:
                    state["petItems"]["door_opened"] = False
                    print("You close the door")
                else:
                    state["petItems"]["door_opened"] = True
                    print("You open the door")
            elif choice == 3 and not state["petMeters"]["sleeping"]:
                state["petMeters"]["fun"] -= 20
                if state["petMeters"]["fun"]:
                    state["petMeters"]["fun"] = 0
                state["petMeters"]["social"] -= 10
                if state["petMeters"]["social"] < 0:
                    state["petMeters"]["social"] = 0
                print("You play with {}".format(state["petName"]))
            elif choice == 4:
                print("You do nothing")
            elif choice == 5:
                for _ in range(47):
                    blockPrint()
                    self.increase_meter(state["petMeters"])
                    bt.execute(state)
                    enablePrint()
            elif choice == 6:
                print("Food bowl is {}% filled".format(state["petItems"]["food_bowl"]))
                print("Door is {}".format("Open" if state["petItems"]["door_opened"] else "Closed"))
                if state["petItems"]["shit_on_floor"]:
                    print("There's a mess on the floor...")
            elif choice == 7:
                if state["petItems"]["shit_on_floor"]:
                    state["petItems"]["shit_on_floor"] = False
                    print("The floor is now clean.")
                else:
                    print("There is no mess to clean!")
            elif choice == 8:
                state["petMeters"]["hygiene"] = 0
                print("You give {} a bath".format(state["petName"]))
            else:
                raise ValueError("Invalid Choice")
        except ValueError as e:
            print("Input is not a choice. Please select a valid choice.")
            self.actions(state, bt)

    def create_behavior_tree(self):
        # Root node for cat
        root = Selector(name='Dog Behaviors')

        # Hygiene branch
        hygiene_sequence = Sequence(name='dog hygiene sequence')
        check_hygiene = Check(dog_check_hygiene)
        shaking = Action(dog_shaking)
        hygiene_sequence.child_nodes = [check_hygiene, shaking]

        dog_priority_selector = DogSelector(name='Dog Priority')

        # Hunger branch
        hunger = Sequence(name='Hunger')
        bowl_selector = Selector(name = 'bowl selector')
        check_bowl = Check(if_bowl_full)
        bark_for_food_action = Action(bark_for_food)
        bowl_selector.child_nodes = [check_bowl, bark_for_food_action]
        eating = Action(eat)
        hunger.child_nodes = [bowl_selector, eating]

        # Bladder branch
        bladder = Sequence(name='Bladder')
        improper_relief_selector = Selector(name='improper relief selector')
        check_door_opened = Check(check_door)
        improper_relief_always_false = AlwaysFalse(name='improper relief always false')
        improper_relief_always_false_selector = Selector(name='improper relief always false selector')
        bark_at_door_sequence = Sequence(name='bark at door sequence')
        check_bladder_full = Check(check_bladder)
        bark_at_door_action = Action(bark_at_door)
        improper_relief_action = Action(improper_relief)
        bark_at_door_sequence.child_nodes = [check_bladder_full, bark_at_door_action]
        improper_relief_always_false_selector.child_nodes = [bark_at_door_sequence, improper_relief_action]
        improper_relief_always_false.child_nodes = [improper_relief_always_false_selector]
        improper_relief_selector.child_nodes = [check_door_opened, improper_relief_always_false]
        dog_proper_relief_action = Action(dog_proper_relief)
        bladder.child_node = [improper_relief_selector, dog_proper_relief_action]

        # Fun branch
        fun = Sequence(name='Fun')
        running_around_action = Action(running_around)
        fun.child_nodes = [running_around_action]

        # Social branch
        social = Sequence(name='Social')
        barking_action = Action(barking)
        social.child_nodes = [barking_action]

        # Energy branch
        energy = Sequence(name='Energy')
        go_to_sleep_action = Action(go_to_sleep)
        energy.child_nodes = [go_to_sleep_action]

        # Sleep branch
        sleep = Sequence(name='Sleep')
        sleeping_action = Action(sleeping)
        sleep.child_nodes = [sleeping_action]

        dog_priority_selector.child_nodes = [hunger, bladder, fun, social, energy, sleep]
        root.child_nodes = [hygiene_sequence, dog_priority_selector]

        return root

    # Increment dog meters over time to represent realistic needs of a dog
    def increase_meter(self, meter):
        for key, val in meter.items():
            if meter['sleeping']:
                if key == 'hunger':
                    meter[key] += 3
                elif key == 'energy':
                    meter[key] += 0
                elif key == 'hygiene':
                    meter[key] += 3
                elif key == 'bladder':
                    meter[key] += 3
                elif key == 'fun':
                    meter[key] += 0
                elif key == 'social':
                    meter[key] += 0
            else:
                if key == 'hunger':
                    meter[key] += 6
                elif key == 'energy':
                    meter[key] += 2
                elif key == 'hygiene':
                    meter[key] += 3
                elif key == 'bladder':
                    meter[key] += 6
                elif key == 'fun':
                    meter[key] += 4
                elif key == 'social':
                    meter[key] += 4

            if val > 100:
                meter[key] = 100

class Cat(Pet):
    def __init__(self, name=None):
        self.name = name
        self.meter = {
            "hunger": 0,
            "energy": 0,
            "bladder": 0,
            "fun": 60,
            "hygiene": 0,
            "social": 36,
            "sleeping": False,
            "ready_to_play": False
        }
        self.item = {
            "food_bowl": 0,
            "litter_box": 100,
            "shit_on_floor": False
        }

    # Available actions for the owner (player) to do
    def actions(self, state, bt):
        print("Available Actions")
        print("1. Fill food bowl")
        print("2. Clean litter box")
        if not state["petMeters"]["sleeping"]:
            print("3. Play with cat")
        print("4. Do nothing")
        print("5. Sleep")
        print("6. Check items")
        print("7. Clean mess")
        print()
        try:
            choice = int(input("Enter the number of the action you want to do: "))
            print()
            if choice == 1:
                state["petItems"]["food_bowl"] = 100
                print("Food bowl has been filled.")
            elif choice == 2:
                state["petItems"]["litter_box"] = 100
                print("Litter box has been cleaned.")
            elif choice == 3 and not state["petMeters"]["sleeping"]:
                if state["petMeters"]["ready_to_play"]:
                    state["petMeters"]["social"] -= 35
                    state["petMeters"]["fun"] -= 30
                    if state["petMeters"]["fun"] < 0:
                        state["petMeters"]["fun"] = 0
                    print("You play with {}.".format(state["petName"]))
                else:
                    print("{} ran away when you tried to play with it!".format(state["petName"]))
            elif choice == 4:
                print("You do nothing")
            elif choice == 5:
                for _ in range(47):
                    blockPrint()
                    self.increase_meter(state["petMeters"])
                    bt.execute(state)
                    enablePrint()
            elif choice == 6:
                print("Food bowl is {}% filled".format(state["petItems"]["food_bowl"]))
                print("Litter box is {}% clean".format(state["petItems"]["litter_box"]))
                if state["petItems"]["shit_on_floor"]:
                    print("There's a mess on the floor...")
            elif choice == 7:
                if state["petItems"]["shit_on_floor"]:
                    state["petItems"]["shit_on_floor"] = False
                    print("The floor is now clean.")
                else:
                    print("There is no mess to clean!")
            else:
                raise ValueError()
        except ValueError as e:
            print("Input is not a choice. Please select a valid choice.")
            self.actions(state, bt)

    # Increment cat meters over time to represent realistic needs of a cat
    def increase_meter(self, meter):
        for key, val in meter.items():
            if meter['sleeping']:
                if key == "hunger":
                    meter[key] += 3
                elif key == "energy":
                    meter[key] += 0
                elif key == 'hygiene':
                    meter[key] += 3
                elif key == 'bladder':
                    meter[key] += 3
                elif key == 'fun':
                    meter[key] += 0
                elif key == 'social':
                    meter[key] += 0
            else:
                if key == 'hunger':
                    meter[key] += 6
                elif key == 'energy':
                    meter[key] += 2
                elif key == 'hygiene':
                    meter[key] += 3
                elif key == 'bladder':
                    meter[key] += 6
                elif key == 'fun':
                    meter[key] += 4
                elif key == 'social':
                    meter[key] += 4
            
            if val > 100:
                meter[key] = 100


    def create_behavior_tree(self):
        # Root node for cat
        root = Sequence(name='Cat Behaviors')

        turn_play_off = Action(playing_reset)
        cat_priority_selector = CatSelector(name='Cat Priority')

        # Hunger Branch
        hunger = Sequence(name='Hunger')

        bowl_checker = Selector(name='Bowl Checker')
        check_food = Check(if_bowl_full)
        call_owner_action = Action(call_owner)
        eat_action = Action(eat)

        hunger.child_nodes = [bowl_checker, eat_action]
        bowl_checker.child_nodes = [check_food, call_owner_action]

        # Fun Branch
        fun = Selector(name='Fun')

        social = Sequence(name='Check Social')
        check_social = Check(social_meter)
        meow_action = Action(meow)
        ready_to_play_action = Action(ready_to_play)
        play_alone_action = Action(play_alone)

        fun.child_nodes = [social, play_alone_action]
        social.child_nodes = [check_social, meow_action, ready_to_play_action]

        # Bladder Branch
        bladder = Selector(name='Bladder')

        proper_relief = Sequence(name='Proper Relief')
        check_box_check = Check(check_box)
        box_relief_action = Action(box_relief)
        improper_relief_action = Action(improper_relief)

        bladder.child_nodes = [proper_relief, improper_relief_action]
        proper_relief.child_nodes = [check_box_check, box_relief_action]

        # Hygiene Branch
        hygiene = Sequence(name='Hygiene')
        clean_self_action = Action(clean_self)
        hygiene.child_nodes = [clean_self_action]

        # Social Branch
        social = Sequence(name='Social')
        meow_action = Action(meow)
        social.child_nodes = [meow_action]

        # Sleep Branch
        energy = Sequence(name='Energy')
        go_to_sleep_action = Action(go_to_sleep)
        energy.child_nodes = [go_to_sleep_action]

        sleep = Sequence(name='Sleep')
        sleeping_action = Action(sleeping)
        sleep.child_nodes = [sleeping_action]

        # Root Children
        cat_priority_selector.child_nodes = [hunger, fun, social, bladder, energy, hygiene, sleep]
        root.child_nodes = [turn_play_off, cat_priority_selector]

        return root

# Fish info
# Selector: What the fish do
# | Sequence: Ensure the fish is fed
# | | Check: if I'm hungry
# | | Action: swim slowly
# | Sequence: Ensure the tank is clean
# | | Check: if the tank is clean
# | | Action: swim_sideways
# | Sequence: Sleep if tired
# | | Check: if the fish is tired
# | | Action: sleep
# | Action: "Idle": swim around normally

class Fish:
    def __init__(self, name=None):
        self.name = name
        self.meter = {
            "hunger": 0,
            "energy": 0,
            "bladder": 0, # abstracted away for time's sake
            "fun": 60, # unused
            "hygiene": 0, # updated but unused
            "social": 36, # unused
            "sleeping": False
        }
        self.item = {
            "food_in_tank": 0,
            "tank_cleanliness": 20
        }


    # Set up the other stuff to reflect the logic in the comment above
    def create_behavior_tree(self):
        # Hunger branch
        hunger = Sequence(name='Hunger')

        tank_food_checker = Sequence(name='Tank Checker')
        check_hungry = Check(is_hungry)
        check_food = Check(food_in_tank)
        swim_action = Action(swim)
        tank_food_checker.child_nodes = [check_food, swim_action]

        eat_action = Action(fish_eat)

        hunger.child_nodes = [check_hungry, tank_food_checker, eat_action]


        # Hygiene branch
        hygiene = Sequence(name='Hygiene')

        clean_tank_check = Check(if_tank_clean)
        swim_sideways_action = Action(swim_sideways)

        hygiene.child_nodes = [clean_tank_check, swim_sideways_action]

        # Sleep branch
        sleep = Sequence(name='Sleep')

        tired_check = Check(is_tired)
        go_to_sleep = Action(sleeping)
        sleep.child_nodes = [tired_check, go_to_sleep]

        # Default/idle
        default = Action(swim)

        # Root node for fish
        root = Selector(name='Fish behaviors')
        root.child_nodes = [hunger, hygiene, sleep, default]

        return root

    # Available actions for the owner (player) to do
    def actions(self, state, bt):
        print("Available Actions")
        print("1. Feed")
        print("2. Clean tank")
        print("3. Do nothing")
        print("4. Sleep")
        print("5. Check items")
        print()
        try:
            choice = int(input("Enter the number of the action you want to do: "))
            print()
            if choice == 1:
                state["petItems"]["food_in_tank"] += 5
                print("You added some food to {}'s tank and {} is eyeing it hungrily.".format(state["petName"], state["petName"]))
            elif choice == 2:
                state["petMeters"]["hygiene"] = max(state["petMeters"]["hygiene"]-30, 0)
                state["petItems"]["tank_cleanliness"] += 20 + random.randint(0, 5)
                print("You cleaned {}'s tank.".format(state["petName"]))
            elif choice == 3:
                pass
            elif choice == 4:
                for _ in range(random.randint(37, 57)):
                    self.increase_meter(state["petMeters"])
                    bt.execute(state)
            elif choice == 5:
                print("Food in tank: {}".format(state["petItems"]["food_in_tank"]))
                print("Tank cleanliness: {}".format(state["petItems"]["tank_cleanliness"]))
            else:
                raise ValueError("Invalid Choice")
        except ValueError as e:
            print("Input is not a choice. Please select a valid choice.")
            self.actions(state, bt)

    # Increment fish meters over time to represent realistic needs of a fish
    def increase_meter(self, meter):
        if random.randint(1, 10) == 10:
            self.item['tank_cleanliness'] = max(self.item['tank_cleanliness']-1, 0)
        
        for key, val in meter.items():
            if meter['sleeping']:
                if key == 'hunger':
                    meter[key] += 3
                elif key == 'energy':
                    meter[key] += 0
                elif key == 'hygiene':
                    meter[key] += 3
                elif key == 'fun':
                    meter[key] += 0
                elif key == 'social':
                    meter[key] += 0
            else:
                if key == 'hunger':
                    meter[key] += 6
                elif key == 'energy':
                    meter[key] += 2
                elif key == 'hygiene':
                    meter[key] += 3
                elif key == 'fun':
                    meter[key] += 4
                elif key == 'social':
                    meter[key] += 4

            if val > 100:
                meter[key] = 100

# ---------------------------------------------------------------------

if __name__ == '__main__':
    try:
        # Read in the state. For now just set it to None
        state = None
        pets = [Dog(), Cat(), Fish()]
        while True:
            for pet in pets:
                pet.increase_meter(state)

    except KeyboardInterrupt:
        print('\nKeyboard interrupt recieved, exiting')
