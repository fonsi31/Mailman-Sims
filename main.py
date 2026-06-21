from definitions import *

def main():
    location = input("Location of Map: ")
    map = load_map(location)
    clear_terminal()
    cities = []

    for loc in map.values():
        if not loc["City"] in cities:
            cities.append(loc["City"])
    
    choice = ""
    while choice != "5":
        clear_terminal()
        for i in range(0, len(cities)):
            print(f"{i+1} - {cities[i]}")
        print(f"{len(cities)+1} - Exit")

        choice = input("Where do you want to start? ")

        match choice:
            case "1":
                pass
            case "2":
                pass
            case "3":
                pass
            case "4":
                pass
            case "5":
                pass
            case _:
                print("Invalid Input!")
                input("Press Enter to continue...")

if __name__ == "__main__":
    main()