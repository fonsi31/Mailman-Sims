import csv
import os
from time import sleep
import shutil


motorcycle = r"""
--------------------         `   `.
       <```--...       .---.//  < `.
         `..     `.___ /       ___`.'
          _ `_.      `      .'\\__
        .'---`.`.          / .'---`.
       /.'  _`.\_\        / /.'\\ `.\
       ||  <__||_|        | ||  ~  ||
       \`.___.'/ /________\ \`.___.'/
        `.___.'              `.___.' 
"""

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def load_map(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r", newline="") as file:
        try:
            reader = csv.reader(file) #reader is now a 2d List
            next(reader, None) #moves the pointer on the 2nd row to skip reading the 1st row
            map = {}
            for line in reader:
                map[line[2]] = {"City": line[0], #The school address or destination will be the key
                                "Post Office": line[1],
                                "Distance": int(line[3])} #Distance of the school from the post office it is located in
                i += 1
            return map
        except (csv.Error, ValueError, IndexError):
            return {}

def display_animation(sorted_mails):
    clear_terminal()


def sort_mails(map, mails, low, high): #Quick Sort
    #sorts the list mails in a descending order
    if low >= high:
        return mails
    pv = low
    i = pv+1 #lower bound
    j = high #upper bound
    pivot_value = map[mails[pv]]["Distance"]
    while i <= j:
        if map[mails[i]]["Distance"] < pivot_value:
            if map[mails[j]]["Distance"] > pivot_value:
                temp = mails[i]
                mails[i] = mails[j]
                mails[j] = temp
                i += 1
                j -= 1
            else:
                j -= 1
        else:
            i += 1
    temp = mails[pv]
    mails[pv] = mails[j]
    mails[j] = temp
    sort_mails(map, mails, low, j-1)
    sort_mails(map, mails, j+1, high)

def deliver_mails(starting_city, map):
    current_city = starting_city
    destinations = [] #A list of school addresses the rider has to deliver to
    diff_cities = [] #A list of different cities the rider has to visit for delivery
    
    cities_visited = 0
    
    print(f"We are going to {current_city} Post Office to get the mails to be delivered")
    print(motorcycle)

    mails_no = input("How many mails are there? ")
    while not mails_no.isdigit() or int(mails_no) < 0:
        mails_no = input("How many mails are there? ")
    
    mails_no = int(mails_no)

    for i in range(0, mails_no): #The user inputs the destination for mail deliveries
        destination = input(f"Destination of mail {i+1}: ")
        while not destination in map:
            destination = input(f"Destination of mail {i+1}: ")
        destinations.append(destination)
        if not map[destination]["City"] in diff_cities:
            diff_cities.append(map[destination]["City"])

    while cities_visited < len(diff_cities):
        clear_terminal()
        if cities_visited >= 1 and len(diff_cities) > 1:
            print("Let us go to the next Post Office.")
            input("Press 'Enter' to go to the next Post Office")
            print(f"We are going to {current_city} Post Office to get the mails to be delivered")
            print(motorcycle)
            mails_no = input("How many mails are there? ")
            while not mails_no.isdigit() or int(mails_no) < 0:
                mails_no = input("How many mails are there? ") #additional mails if the user wants to add
            mails_no = int(mails_no)
            new_cities = []
            for i in range(0, mails_no): #The user inputs the destination for mail deliveries
                destination = input(f"Destination of mail {i+1}: ")
                while not destination in map:
                    destination = input(f"Destination of mail {i+1}: ")
                destinations.append(destination)
                if not map[destination]["City"] in new_cities:
                    new_cities.append(map[destination]["City"])
            diff_cities.extend(new_cities)
        
        segregated_mails = [] #destinations will be grouped accordingly by the city they're located in
        for place in destinations: #Segregates mails by the city of its destination
            if map[place]["City"] == current_city:
                segregated_mails.append(place)

        sort_mails(map, segregated_mails, 0, len(segregated_mails)-1)
        display_animation(segregated_mails)
        clear_terminal()
        print(motorcycle)
        print(f"{current_city} Post Office")
        print(f"All mails for {current_city} are delivered!")
        cities_visited += 1 
        current_city = diff_cities[cities_visited]
    
    print("We are done for today, but you may choose to deliver new mails for other Post Offices again")
    input("Press 'Enter' to go back to the Main Menu")