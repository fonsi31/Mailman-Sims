from definitions import *

def main():
    location = input("Location of Map: ")
    delivery_map = load_map(location)
    clear_terminal()
    cities = []
    
    for loc in delivery_map.values():
        if not loc["City"] in cities:
            cities.append(loc["City"])
    
    if len(cities) < 1:
        print("Failed to load map!")
    else:
        choice = ""
        while choice != len(cities) + 1:
            clear_terminal()
            for i in range(0, len(cities)):
                print(f"{i+1} - {cities[i]}")
            print(f"{len(cities)+1} - Exit")

            choice = input("Where do you want to start? ")

            if choice.isdigit():
                choice = int(choice)
                if choice >= 1 and choice <= len(cities):
                    deliver_mails(cities[choice-1], delivery_map)
                elif choice < 1 or choice > len(cities) + 1:
                    print("Invalid Input")
                    input("Press enter to continue...")
            else:
                print("Invalid Input!")
                input("Press enter to continue...")

if __name__ == "__main__":
    main()