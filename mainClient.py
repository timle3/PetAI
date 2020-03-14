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
    petMeters = pet.create_meter()
    petItems = pet.create_item()
    gamestate = {
        "petMeters" : petMeters,
        "petItems" = petItems}
    }

    while(True):
        pet.increase_meter(petMeters)
        pet.execute(gamestate)
        pet.actions(gamestate)
        print()