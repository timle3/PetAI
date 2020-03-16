from pets import *


if __name__ == "__main__":
    # Choosing which pet to adopt
    print("Welcome to PetAI! Please select what kind of pet you would like.")
    petList = ["Fish", "Dog", "Cat"]
    try:
        for i, pet in enumerate(petList):
            print("{}. {}".format(i+1, pet))
        choice = input().lower()
        index = next(i for i, petList in enumerate(petList) if petList.lower() == choice)
    except StopIteration as e:
        print("Input is not a choice. Please select a valid choice next time.")
        print("Exiting...")
        exit()

    # Naming pet
    print("You have adopted a new {}, what would you like to name it?".format(petList[index]))
    name = input()
    pet = eval(petList[index])(name)
    print()
    
    # Pet initialized, behaviors will now start and react to owner actions
    petBT = pet.create_behavior_tree()
    gamestate = {
        "petMeters" : pet.meter,
        "petItems": pet.item,
        "petName": pet.name
    }

    while(True):
        print(gamestate["petMeters"])
        print(gamestate["petItems"])
        petBT.execute(gamestate)
        pet.actions(gamestate, petBT)
        print()
        pet.increase_meter(pet.meter)