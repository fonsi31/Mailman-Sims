from definitions import *

def main():
    location = input("Location of Map: ")
    delivery_map = load_map(location)
    clear_terminal()
    cities = []
    
    for loc in delivery_map.values():
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
                deliver_mails(cities[0], delivery_map)
            case "2":
                deliver_mails(cities[1], delivery_map)
            case "3":
                deliver_mails(cities[2], delivery_map)
            case "4":
                deliver_mails(cities[3], delivery_map)
            case "5":
                break
            case _:
                print("Invalid Input!")
                input("Press Enter to continue...")

if __name__ == "__main__":
    main()