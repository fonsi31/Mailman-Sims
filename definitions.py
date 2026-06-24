import csv
import os
from time import sleep
import shutil

motorcycle = r"""
--------------------         `   `.
       <```--...       .---.//  < `.
         `..     `.___ /       ___`.'
          _ `_.       `     .'\\__
        .'---`.`.          / .'---`.
       /.'  _`.\_\        / /.'\\ `.\
       ||  <__||_|        | ||  ~  ||
       \`.___.'/ /________\ \`.___.'/
        `.___.'              `.___.' 
"""

terminal_width = shutil.get_terminal_size().columns
motorcycle_width = max(len(line) for line in motorcycle.splitlines())
motorcycle_center = (motorcycle_width // 2) + 6 #Added 6 units since the cargo box forces the center to go further left of the motorcycle

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def load_map(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)

    if not os.path.exists(file_path):
        print("File not found!")
        return {}

    with open(file_path, "r", newline="") as file:
        try:
            reader = csv.reader(file) #reader is now a 2d List
            next(reader, None) #moves the pointer on the 2nd row to skip reading the 1st row
            delivery_map = {}
            for line in reader:
                delivery_map[line[2]] = {"City": line[0], #The school address or destination will be the key
                                "Post Office": line[1],
                                "Distance": float(line[3])} #Distance of the school from the post office it is located in
            return delivery_map
        except Exception as e:
            print("ERROR: ", e)
            return {}
     
def display_animation(sorted_mails, current_city):
    clear_terminal()
    post_office = current_city + " Post Office"
    road = "-" * 25

    route = """"""
    shift_right = " " * 8 # shifts the route by n units of white spaces to the right
    route = shift_right + " " * (len(post_office) // 2) + "○" + "\n" + shift_right + post_office #base form of the route
    routes = []
    dropoff_points = []
    reversed_lst = sorted_mails[::-1] #since the mails are sorted in a descending order (by distance), we need to reverse it to draw the correct route
    for mail in reversed_lst: #Draw route
        before = route #take a snapshot of the route before you add another road in case the route will be too long after adding another road
        lines = route.splitlines()
        lines[0] += road + "○"
        dropoff_points.append(len(lines[0]))
        route = "\n".join(lines)   
        route += " " * 6 + mail[:19]
        route_width = max(len(line) for line in route.splitlines())
        if route_width >= terminal_width:
            dropoff_points.pop()
            routes.append(before)
            route = shift_right + " " * (len(post_office) // 2) + "○" + "\n" + shift_right + post_office #reset route to its base form and add remaining roads
            lines = route.splitlines()
            lines[0] += road + "○"
            dropoff_points.append(len(lines[0]))
            route = "\n".join(lines)
            route += " " * 6 + mail[:19]
    routes.append(route)

    position = 0 
    i = 0 # index of the current route visible on the terminal
    j = 0 #index for the current dropoff point
    while len(sorted_mails) > 0:
        deliveries = """"""
        for mail in sorted_mails: #draws the cargo box
            deliveries = "|" + mail[:19] + "|\n" + deliveries
            deliveries = "--------------------\n" + deliveries
        deliveries = deliveries.rstrip("\n")
        figure = deliveries + motorcycle
        flag = True #permission to print the figure
        offset = " " * position
        frame = "\n".join(offset + line for line in figure.splitlines()) #keeps appending space before the frame making it look like its moving
        if motorcycle_width + len(offset) >= terminal_width:
            position = -1
            flag = False
            if i < len(routes):
                i += 1
        print(position + motorcycle_center, dropoff_points[j])
        if position + motorcycle_center == dropoff_points[j]:
            sorted_mails.pop()
            if j < len(dropoff_points):
                j += 1
        position += 1
        if flag:
            print(frame)
        print(routes[i])
        sleep(0.25)
        clear_terminal()

    #draw and print the figure one last time
    deliveries = """"""
    for mail in sorted_mails: #draws the cargo box
        deliveries = "|" + mail[:19] + "|\n" + deliveries
        deliveries = "--------------------\n" + deliveries
    deliveries = deliveries.rstrip("\n")
    figure = deliveries + motorcycle
    offset = " " * position
    frame = "\n".join(offset + line for line in figure.splitlines())
    return frame + "\n" + routes[i]

def sort_mails(delivery_map, mails, low, high): #Quick Sort
    #sorts the mails in a descending order (by distance)
    if low >= high:
        return mails
    pv = low #pivot index
    i = pv+1 #lower bound
    j = high #upper bound
    pivot_value = delivery_map[mails[pv]]["Distance"]
    while i <= j:
        if delivery_map[mails[i]]["Distance"] < pivot_value:
            if delivery_map[mails[j]]["Distance"] > pivot_value:
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
    sort_mails(delivery_map, mails, low, j-1)
    sort_mails(delivery_map, mails, j+1, high)

def deliver_mails(starting_city, delivery_map):
    clear_terminal()
    current_city = starting_city
    destinations = [] #A list of school addresses the rider has to deliver to
    diff_cities = [] #A list of different cities the rider has to visit for delivery
    diff_cities.append(starting_city)
    
    cities_visited = 0
    
    print(f"We are going to {current_city} Post Office to get the mails to be delivered")
    print(motorcycle)

    mails_no = input("How many mails are there? ")
    while not mails_no.isdigit() or int(mails_no) < 0:
        mails_no = input("How many mails are there? ")
    
    mails_no = int(mails_no)

    for i in range(0, mails_no): #The user inputs the destination for mail deliveries
        destination = input(f"Destination of mail {i+1}: ")
        while destination not in delivery_map:
            destination = input(f"Destination of mail {i+1}: ")
        if destination not in destinations:
            destinations.append(destination)
        if not delivery_map[destination]["City"] in diff_cities:
            diff_cities.append(delivery_map[destination]["City"])

    while cities_visited < len(diff_cities):
        if cities_visited >= 1 and len(diff_cities) > 1:
            print("Let us go to the next Post Office.")
            input("Press 'Enter' to go to the next Post Office")
            clear_terminal()
            current_city = diff_cities[cities_visited]
            print(f"We are going to {current_city} Post Office to get the mails to be delivered")
            print(motorcycle)
            mails_no = input("How many mails are there? ")
            while not mails_no.isdigit() or int(mails_no) < 0:
                mails_no = input("How many mails are there? ") #additional mails if the user wants to add
            mails_no = int(mails_no)
            new_cities = []
            for i in range(0, mails_no): #The user inputs the destination for mail deliveries
                destination = input(f"Destination of mail {i+1}: ")
                while destination not in delivery_map:
                    destination = input(f"Destination of mail {i+1}: ")
                if destination not in destinations:
                    destinations.append(destination)
                if delivery_map[destination]["City"] not in new_cities:
                    new_cities.append(delivery_map[destination]["City"])
            diff_cities.extend(new_cities)
        
        segregated_mails = [] #destinations will be grouped accordingly by the city they're located in
        for place in destinations[:]: #Segregates mails by the city of its destination
            if delivery_map[place]["City"] == current_city:
                segregated_mails.append(place)
                destinations.remove(place)

        if len(segregated_mails) > 0: 
            sort_mails(delivery_map, segregated_mails, 0, len(segregated_mails)-1)
            figure = display_animation(segregated_mails, current_city)
            if cities_visited == len(diff_cities) - 1:
                print(figure)
            else:
                post_office = current_city + " Post Office"
                motorcycle_copy = motorcycle
                motorcycle_copy = motorcycle_copy.rstrip("\n")
                print(motorcycle_copy)
                print(" " * (motorcycle_width//2-8) + " " * (len(post_office) // 2) + "○")
                print(" " * (motorcycle_width//2-8) + post_office)
            print()
            print(f"All mails for {current_city} are delivered!")
        cities_visited += 1 
    
    print("We are done for today, but you may choose to deliver new mails for other Post Offices again")
    input("Press 'Enter' to go back to the Main Menu")