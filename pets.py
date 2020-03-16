from bt_nodes import *
from checks import *
from behaviors import *
import random

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
        print("3. Play with dog")
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
            elif choice == 3:
                if state["petMeters"]["ready_to_play"]:
                    state["petMeters"]["social"] -= 35
                    state["petMeters"]["fun"] -= 30
                    if state["petMeters"]["fun"] < 0:
                        state["petMeters"]["fun"] = 0
                    print("You play with the cat.")
                else:
                    print("The cat ran away when you tried to play with it!")
            elif choice == 4:
                pass
            elif choice == 5:
                for _ in range(47):
                    self.increase_meter(state["petMeters"])
                    bt.execute(state)
            elif choice == 6:
                print("Food bowl is {}% filled".format(state["petItems"]["food_bowl"]))
                print("Litter box is {}% clean".format(state["petItems"]["litter_box"]))
            elif choice == 7 and state["petItems"]["shit_on_floor"] == True:
                print("The floor is now clean.")
            elif choice == 7 and state["petItems"]["shit_on_floor"] == False:
                print("There is no mess to clean!")
            else:
                raise ValueError("Invalid Choice")
        except ValueError as e:
            print("Input is not a choice. Please select a valid choice.")
            self.actions(state, bt)


    def create_behavior_tree(self):
        # Root node for cat
        root = Sequence(name='Dog Behaviors')

        hygiene_always_false = AlwaysFalse(name='dog hygiene always false')
        hygiene_sequence = Sequence(name='dog hygiene sequence')
        check_hygiene = Check(dog_check_hygiene)
        shaking = Action(dog_shaking)
        hygiene_sequence.child_nodes = [check_hygiene, shaking]
        hygiene_always_false.child_node = [hygiene_sequence]

        dog_priority_selector = DogSelector(name='Dog Priority')

        hunger = Sequence(name='hunger')
        bowl_selector = Selector(name = 'bowl selector')
        check_bowl = Check(if_bowl_full)
        bark_for_food_action = Action(bark_for_food)
        bowl_selector.child_node = [check_bowl, bark_for_food]
        eating = Action(eat)
        hunger.child_node = [bowl_selector, eating]

        bladder = Sequence(name='bladder')
        improper_relief_selector = Selector(name= 'improper relief selector')
        check_door_opened = Check(check_door)
        improper_relief_always_false = AlwaysFalse(name = 'improper relief always false')
        improper_relief_always_false_selector = Selector(name = 'improper relief always false selector')
        bark_at_door_sequence = Sequence(name = 'bark at door sequence')
        check_bladder_full = Check(check_bladder)
        bark_at_door_action = Action(bark_at_door)
        improper_relief_action = Action(improper_relief)
        bark_at_door_sequence.child_node = [check_bladder_full, bark_at_door_action]
        improper_relief_always_false_selector.child_node = [bark_at_door_sequence, improper_relief_action]
        improper_relief_always_false.child_node = [improper_relief_always_false_selector]
        improper_relief_selector.child_node = [check_door_opened, improper_relief_always_false]
        dog_proper_relief_action = Action(dog_proper_relief)
        bladder.child_node = [improper_relief_selector, dog_proper_relief_action]
        
        improper_relief_selector.child_node = [check_door, improper_relief_always_false]
        dog_proper_relief = Action(dog_proper_relief)
        bladder.child_node = [improper_relief_selector, dog_proper_relief]

        fun = Sequence(name='fun')
        running_around_action = Action(running_around)
        fun.child_node = [running_around_action]

        social = Sequence(name='social')
        barking_action = Action(barking)
        social.child_node = [barking_action]

        energy = Sequence(name='energy')
        go_to_sleep_action = Action(go_to_sleep)
        energy.child_nodes = [go_to_sleep_action]

        sleep = Sequence(name='sleep')
        sleeping_action = Action(sleeping)
        sleep.child_nodes = [sleeping_action]

        dog_priority_selector.child_node = [hunger, bladder, fun, social, energy, sleep]
        root.child_node = [hygiene_always_false, dog_priority_selector]
        return root

    # Increment dog meters over time to represent realistic needs of a dog
    def increase_meter(self, meter):
        numMeter = ["hunger", "energy", "bladder", "fun", "hygiene", "social"]
        for key, val in meter.items():
            if key == 'hunger' and meter['sleeping'] == True:
                meter[key] += 3
            if key == 'hunger' and meter['sleeping'] == False:
                meter[key] += 6

            if key == 'energy' and meter['sleeping'] == True:
                meter[key] += 0
            if key == 'energy' and meter['sleeping'] == False:
                meter[key] += 2

            if key == 'hygiene' and meter['sleeping'] == True:
                meter[key] += 3
            if key == 'hygiene' and meter['sleeping'] == False:
                meter[key] += 3

            if key == 'bladder' and meter['sleeping'] == True:
                meter[key] += 3
            if key == 'bladder' and meter['sleeping'] == False:
                meter[key] += 6

            if key == 'fun' and meter['sleeping'] == True:
                meter[key] += 0
            if key == 'fun' and meter['sleeping'] == False:
                meter[key] += 4

            if key == 'social' and meter['sleeping'] == True:
                meter[key] += 0
            if key == 'social' and meter['sleeping'] == False:
                meter[key] += 4

            if meter[key] > 100:
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
            elif choice == 3:
                if state["petMeters"]["ready_to_play"]:
                    state["petMeters"]["social"] -= 35
                    state["petMeters"]["fun"] -= 30
                    if state["petMeters"]["fun"] < 0:
                        state["petMeters"]["fun"] = 0
                    print("You play with the cat.")
                else:
                    print("The cat ran away when you tried to play with it!")
            elif choice == 4:
                pass
            elif choice == 5:
                for _ in range(47):
                    self.increase_meter(state["petMeters"])
                    bt.execute(state)
            elif choice == 6:
                print("Food bowl is {}% filled".format(state["petItems"]["food_bowl"]))
                print("Litter box is {}% clean".format(state["petItems"]["litter_box"]))
            elif choice == 7 and state["petItems"]["shit_on_floor"] == True:
                print("The floor is now clean.")
            elif choice == 7 and state["petItems"]["shit_on_floor"] == False:
                print("There is no mess to clean!")
            else:
                raise ValueError("Invalid Choice")
        except ValueError as e:
            print("Input is not a choice. Please select a valid choice.")
            self.actions(state, bt)

    # Increment cat meters over time to represent realistic needs of a cat
    def increase_meter(self, meter):
        numMeter = ["hunger", "energy", "bladder", "fun", "hygiene", "social"]
        for key, val in meter.items():
            if key == 'hunger' and meter['sleeping'] == True:
                meter[key] += 3
            if key == 'hunger' and meter['sleeping'] == False:
                meter[key] += 6

            if key == 'energy' and meter['sleeping'] == True:
                meter[key] += 0
            if key == 'energy' and meter['sleeping'] == False:
                meter[key] += 2

            if key == 'hygiene' and meter['sleeping'] == True:
                meter[key] += 3
            if key == 'hygiene' and meter['sleeping'] == False:
                meter[key] += 3

            if key == 'bladder' and meter['sleeping'] == True:
                meter[key] += 3
            if key == 'bladder' and meter['sleeping'] == False:
                meter[key] += 6

            if key == 'fun' and meter['sleeping'] == True:
                meter[key] += 0
            if key == 'fun' and meter['sleeping'] == False:
                meter[key] += 4

            if key == 'social' and meter['sleeping'] == True:
                meter[key] += 0
            if key == 'social' and meter['sleeping'] == False:
                meter[key] += 4

            if meter[key] > 100:
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

        logging.info('\n' + root.tree_to_string())
        return root

        # Increment fish meters over time to represent realistic needs of a fish
    def increase_meter(self, meter):
        numMeter = ["hunger", "energy", "bladder", "fun", "hygiene", "social"]
        for key, val in meter.items():
            if key == 'hunger' and meter['sleeping'] == True:
                meter[key] += 3
            if key == 'hunger' and meter['sleeping'] == False:
                meter[key] += 6

            if key == 'energy' and meter['sleeping'] == True:
                meter[key] += 0
            if key == 'energy' and meter['sleeping'] == False:
                meter[key] += 2

            if key == 'hygiene' and meter['sleeping'] == True:
                meter[key] += 3
            if key == 'hygiene' and meter['sleeping'] == False:
                meter[key] += 3

            if key == 'bladder' and meter['sleeping'] == True:
                meter[key] += 3
            if key == 'bladder' and meter['sleeping'] == False:
                meter[key] += 6

            if key == 'fun' and meter['sleeping'] == True:
                meter[key] += 0
            if key == 'fun' and meter['sleeping'] == False:
                meter[key] += 4

            if key == 'social' and meter['sleeping'] == True:
                meter[key] += 0
            if key == 'social' and meter['sleeping'] == False:
                meter[key] += 4



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
    def __init__(self):
        self.bt_root = Selector(name='What the fish do')
        # Set up the other stuff to reflect the logic above

        # Root node for fish
        root = Sequence(name='Fish behaviors')
        root.child_nodes = [hunger, hygiene, sleep, default]

        # Hunger branch
        hunger = Sequence(name='Hunger')

        bowl_checker = Sequence(name='Bowl Checker')
        check_food = Check(if_bowl_full)
        swim = Action(swim)

        eat = Action(eat)

        hunger.child_nodes = [bowl_checker, eat]
        bowl_checker.child_nodes = [check_food, swim]


        # Hygiene branch
        hygiene = Sequence(name='Hygiene')

        clean_tank = Sequence(name='Clean Tank')
        clean_tank_check = Check(if_bowl_clean)
        swim_sideways = Action(swim_sideways)

        hygiene.child_nodes = [clean_tank]
        clean_tank.child_nodes = [clean_tank_check, swim_sideways]

        # Sleep branch
        sleep = Sequence(name='Sleep')

        tired_check = Check(if_tired)
        go_to_sleep = Action(sleeping)
        sleep.child_nodes = [tired_check, go_to_sleep]

        # Default/idle
        default = Action(swim)


    # Increment fish meters over time to represent realistic needs of a fish
    def increase_meter(self, meter):
        numMeter = ["hunger", "energy", "bladder", "fun", "hygiene", "social"]
        for key, val in meter.items():
            if key == 'hunger' and meter['sleeping'] == True:
                meter[key] += 3
            if key == 'hunger' and meter['sleeping'] == False:
                meter[key] += 6

            if key == 'energy' and meter['sleeping'] == True:
                meter[key] += 0
            if key == 'energy' and meter['sleeping'] == False:
                meter[key] += 2

            if key == 'hygiene' and meter['sleeping'] == True:
                meter[key] += 3
            if key == 'hygiene' and meter['sleeping'] == False:
                meter[key] += 3

            if key == 'bladder' and meter['sleeping'] == True:
                meter[key] += 3
            if key == 'bladder' and meter['sleeping'] == False:
                meter[key] += 6

            if key == 'fun' and meter['sleeping'] == True:
                meter[key] += 0
            if key == 'fun' and meter['sleeping'] == False:
                meter[key] += 4

            if key == 'social' and meter['sleeping'] == True:
                meter[key] += 0
            if key == 'social' and meter['sleeping'] == False:
                meter[key] += 4


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
