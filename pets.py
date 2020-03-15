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
    def execute(self):
        pass

class Cat(Pet):

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
            "ready_to_play": False
        }
        self.item = {
            "food_bowl": 0,
            "litter_box": 100,
            "shit_on_floor": 0
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
                print(choice)
            elif choice == 4:
                pass
            elif choice == 5:
                for _ in range(47):
                    self.increase_meter(state["petMeters"])
                    bt.execute(state)
            elif choice == 6:
                print("Food bowl is {}% filled".format(state["petItems"]["food_bowl"]))
                print("Litter box is {}% clean".format(state["petItems"]["litter_box"]))
            else:
                raise ValueError("Invalid Choice")
        except ValueError as e:
            print("Input is not a choice. Please select a valid choice.")
            self.actions(state, bt)

    # Increment cat meters over time to represent realistic needs of a cat
    def increase_meter(self, meter):
        numMeter = ["hunger", "energy", "bladder", "fun", "hygiene", "social"]
        for key, val in meter.items():
            if key in numMeter and val < 100:
                meter[key] += 1

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
        energy = Sequence(name='energy')
        go_to_sleep_action = Action(go_to_sleep)
        energy.child_nodes = [go_to_sleep_action]

        sleep = Sequence(name='sleep')
        sleeping_action = Action(sleeping)
        sleep.child_nodes = [sleeping_action]

        # Root Children
        cat_priority_selector.child_nodes = [hunger, fun, social, bladder, energy, hygiene, sleep]
        root.child_nodes = [turn_play_off, cat_priority_selector]
        
        logging.info('\n' + root.tree_to_string())
        return root
    

# Fish info
# Selector: What the fish do
# | Sequence: Ensure the fish is fed
# | | Check: if the tanks is clean
# | | Check: if a human is nearby
# | | Check: if I'm not already swimming slowly
# | | Action: swim slowly
# | Sequence: Ensure the tank is clean
# | | Check: if the tank is clean
# | | Check: if_not_swimming_sideways
# | | Action: swim_sideways

class Fish:
    def __init__(self):
        self.bt_root = Selector(name='What the fish do')
        # Set up the other stuff to reflect the logic above

    def tick(self, state):
        self.bt_root.execute(state)

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
