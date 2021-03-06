from copy import deepcopy
import random
import math

############################### Base Classes ##################################
class Node:
    def __init__(self):
        raise NotImplementedError

    def execute(self, state):
        raise NotImplementedError

    def copy(self):
        return deepcopy(self)


class Composite(Node):
    def __init__(self, child_nodes=[], name=None):
        self.child_nodes = child_nodes
        self.name = name

    def execute(self, state):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.name if self.name else ''

    def tree_to_string(self, indent=0):
        string = '| ' * indent + str(self) + '\n'
        for child in self.child_nodes:
            if hasattr(child, 'tree_to_string'):
                string += child.tree_to_string(indent + 1)
            else:
                string += '| ' * (indent + 1) + str(child) + '\n'
        return string


############################### Composite Nodes ##################################
class DogSelector(Composite):
    def execute(self, state):
        highest_priority = ((state["petMeters"]["hunger"] ** 2) / 320) + (state["petMeters"]["hunger"] / 3)
        code = "Hunger"

        temp = ((state["petMeters"]["energy"] ** 2) / 320) + (state["petMeters"]["energy"] / 3)
        if temp > highest_priority:
            highest_priority = temp
            code = "Energy"

        temp = 500 * (math.cos((state["petMeters"]["bladder"] - 100) / 100)) ** 1000
        if temp > highest_priority:
            highest_priority = temp
            code = "Bladder"

        temp = state["petMeters"]["fun"] / 2
        if temp > highest_priority:
            highest_priority = temp
            code = "Fun"

        temp = state["petMeters"]["social"] / 2
        if temp > highest_priority:
            highest_priority = temp
            code = "Social"
        
        if state["petMeters"]["sleeping"] and (highest_priority < 35 or code == "Energy") :
            for child_node in self.child_nodes:
                if child_node.name == "Sleep":
                    return child_node.execute(state)

        else:
            if state["petMeters"]["sleeping"]:
                print("{} wakes up".format(state["petName"]))
            state["petMeters"]["sleeping"] = False
            for child_node in self.child_nodes:
                if child_node.name == code:
                    return child_node.execute(state)


class CatSelector(Composite):
    def execute(self, state):
        highest_priority = ((state["petMeters"]["hunger"] ** 2) / 320) + (state["petMeters"]["hunger"] / 3)
        code = "Hunger"

        temp = ((state["petMeters"]["energy"] ** 2) / 320) + (state["petMeters"]["energy"] / 3)
        if temp > highest_priority:
            highest_priority = temp
            code = "Energy"

        temp = 500 * (math.cos((state["petMeters"]["bladder"] - 100) / 100)) ** 1000
        if temp > highest_priority:
            highest_priority = temp
            code = "Bladder"

        temp = state["petMeters"]["fun"] / 2
        if temp > highest_priority:
            highest_priority = temp
            code = "Fun"

        temp = state["petMeters"]["hygiene"] / 2
        if temp > highest_priority:
            highest_priority = temp
            code = "Hygiene"

        temp = state["petMeters"]["social"] / 2
        if temp > highest_priority:
            highest_priority = temp
            code = "Social"

        if state["petMeters"]["sleeping"] and (highest_priority < 35 or code == "Energy"):
            for child_node in self.child_nodes:
                if child_node.name == "Sleep":
                    return child_node.execute(state)

        else:
            if state["petMeters"]["sleeping"]:
                print("{} wakes up".format(state["petName"]))
            state["petMeters"]["sleeping"] = False
            for child_node in self.child_nodes:
                if child_node.name == code:
                    return child_node.execute(state)

class Selector(Composite):
    def execute(self, state):
        for child_node in self.child_nodes:
            success = child_node.execute(state)
            if success:
                return True
        else:  # for loop completed without success; return failure
            return False


class Sequence(Composite):
    def execute(self, state):
        for child_node in self.child_nodes:
            continue_execution = child_node.execute(state)
            if not continue_execution:
                return False
        else:  # for loop completed without failure; return success
            return True

class AlwaysTrue(Composite):
    def execute(self, state):
        for child_node in self.child_nodes:
            child_node.execute(state)
        return True

class AlwaysFalse(Composite):
    def execute(self, state):
        for child_node in self.child_nodes:
            child_node.execute(state)
        return False



############################### Decorator Nodes ##################################

class Inverter(Composite):
    def execute(self, state):
        return not self.child_nodes[0].execute(state)


class Succeeder(Composite):
    def execute(self, state):
        self.child_nodes[0].execute(state)
        return True

class Repeater(Composite):
    def execute(self, state, max_iterations=-1):
        iterations = 0
        while iterations != max_iterations and self.child_nodes[0].execute(state) != None:
            iterations += 1
        return

class RepeatUntilFail(Composite):
    def execute(self, state):
        while self.child_nodes[0].execute(state):
            pass
        return True

class Probability(Composite):
    def execute(self, state, chance=0.5):
        if(random.random() < chance):
            return self.child_nodes[0].execute(state)
        else:
            return False

############################### Leaf Nodes ##################################
class Check(Node):
    def __init__(self, check_function):
        self.check_function = check_function

    def execute(self, state):
        return self.check_function(state)

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.check_function.__name__


class Action(Node):
    def __init__(self, action_function):
        self.action_function = action_function

    def execute(self, state):
        return self.action_function(state)

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.action_function.__name__