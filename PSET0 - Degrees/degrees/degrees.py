import csv
import sys

# import the frontier functions to start searching
from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

# Loads data from the CSV files
def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people.csv file, as f
    with open(f"{directory}/people.csv", encoding="utf-8") as f:

        # read f
        reader = csv.DictReader(f)

        # for each person in the file, create an object
        for row in reader:

            people[row["id"]] = {
                "name": row["name"], # name of the person
                "birth": row["birth"], # birthdate of the person
                "movies": set() # create an empty set to be populated with movies the person has done
            }

            # checking to see if there is no duplicates; original name
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]} # populate names with the relevant id

            # if there is a duplicate in names, create new id
            else:
                names[row["name"].lower()].add(row["id"]) # populate names with a new relevant id

    # Load movies.csv file as f
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:

        # read csv file
        reader = csv.DictReader(f)

        # for movie in movies.csv
        for row in reader:

            # create a new object in the movies set
            movies[row["id"]] = {
                "title": row["title"], # title of the movie in the object
                "year": row["year"], # year of the movie in the object
                "stars": set() # create an empty set to be populated with the stars
            }

    # Load stars.csv, basically the file that has the actors and their corresponding movies in ids
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:

        # as always, read the reader file
        reader = csv.DictReader(f)

        # now read each row of the file
        for row in reader:

            try:
                people[row["person_id"]]["movies"].add(row["movie_id"]) # add movie id to the empty set of the person
                movies[row["movie_id"]]["stars"].add(row["person_id"]) # add person id to the empty set of the movie

            except KeyError: # tried to access a key that is not there in the dictionary
                pass # move on to the next row


def main():

    # if the command has more than two, then produce error
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")

    # the directory large or small is inserted into "dictionary" variable, else use large as default
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    # now ask for a source name (the initial name, or the initial state)
    source = person_id_for_name(input("Name: ")) # check the name for duplicate actors and reconcile the differences
    # if there is no source name
    if source is None:
        sys.exit("Person not found.")
    # ask again for the target name
    target = person_id_for_name(input("Name: "))
    # when there is no target name
    if target is None:
        sys.exit("Person not found.")

    # create a path, whereby path is the shortest path between the source and the target actors
    path = shortest_path(source, target)

    # if there is no degrees of seperation between the actors
    if path is None:
        print("Not connected.")

    # else, can input the degrees of seperation into word
    else:
        # degrees is the counting of the path
        degrees = len(path)
        # print out the degrees of seperation in a sentence
        print(f"{degrees} degrees of separation.")

        path = [(None, source)] + path
        # now start printing out the actors and the degrees of seperation, so for i = 1, i = 2, etc
        for i in range(degrees):
            # the first person
            person1 = people[path[i][1]]["name"]
            # the second person
            person2 = people[path[i + 1][1]]["name"]
            # the movie they starred in
            movie = movies[path[i + 1][0]]["title"]
            # the final sentence including the actors and the movie that they starred in
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


# this is the algorithm to code
def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """
    # TODO - let's try a breadth-first search algorithm, because you want the shortest path not the fastest path

    # let's first create a counter, so that we can calculate the path cost of each given path to find shortest path
    num_explored = 0

    # let's initialize a starting point, initialize frontier to the starting position
    start = Node(state = source, parents = None, action = None)

    # now let's initialize the frontier, since we are using a breadth-first search algorithm let's initialize the queue
    frontier = QueueFrontier()
    frontier.add(start) # this frontier now just contains the starting node, with nothing

    # now let's create an empty explored set
    explored = set()

    # now we want to keep looping through until the solution is found
    while True:

        # if there is nothing left in the frontier, then that means there is no path from the source actor to the target actor
        if frontier.empty():
            return None # because there is no path

        # we need to take out a frontier from the node so that we can explore the neighbors of the node to find any target nodes
        node = frontier.remove() # so remove a node from the frontier and add it to the explored set as well as leave it open
        explored += 1 # update the number of states that we have explored

        # mark the current actor as explored so that we will not accidentally search nodes that we have already explored
        explored.add(node)

        # now find all of the possible neighbours for the current node
        neighbors = neighbors_for_person(node.state)
        # and now
        for movie, actor in neighbors: # as a reminder, neighbors contains a set of (movie_id, person_id)
            # if actor is not in the explored set, and not in the frontier set, then
            if actor not in explored and not frontier.contains_state(actor):
                """
                then we create a child node, with state being the current person_id,
                parent being previous node removed, and action to get to the child being the movie_id
                """
                child = Node(state = actor, parent = node, action = movie)
                # and then we want to check if the child node is the answer
                if child.state == target: # whereby child.state is person_id and target is person_id
                    # we now need to figure out the pathway to the target
                    path = [] # initialize an empty path
                    node = child # set node to be the child
                    # so we need to go back upwards from the child all the way to the initial node to see how many states we went through
                    while node.parent is not None:
                        path.append(node.action, node.state) # basically adding the action and the state to the path
                        node = node.parent # setting he node to the parent node, so that we can continue the while loop
                    # to find the initial state downwards
                    path.reverse()
                    return path

                # if the child node is not the target node, then just add the child node to the frontier, so that we don't need to test it
                frontier.add(child)

def person_id_for_name(name): # this is because sometime multiple actors may share a specific name
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    # now get the value from the key in the names dictionary. basically get the id from the name in names
    person_ids = list(names.get(name.lower(), set())) # create a list with value of key, if not create empty set

    # if there are no person ids
    if len(person_ids) == 0:
        return None

    # if there are person ids
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        # for each person id in the list of possible people
        for person_id in person_ids:
            person = people[person_id] # set the person
            name = person["name"] # get the name of the person
            birth = person["birth"] # get the birth of the person
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}") # print the name of the person

        try: # now try and give input into what the intended person id is
            person_id = input("Intended Person ID: ")
            if person_id in person_ids: # if the person id is in the list of possbile people ids for the specific name
                return person_id # return the person id so that the source variable has a person id variable

        except ValueError: # if not than it is an error
            pass # and you should return none
        return None

    else: # else if there is only 1 possible actor, than just return the person id and we can begin
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    # creates a movie_ids list of movies that a particular actor person_id input has filmed in
    movie_ids = people[person_id]["movies"]
    # create a set of neighbours (actors that have acted alongside the person_id)
    neighbors = set()
    # now iterate through the movie_ids list, checking each movie for possible actors one movie at a time
    for movie_id in movie_ids:
        # find actors that have took part in the specified movie or movie_id and include them into the set
        for person_id in movies[movie_id]["stars"]:
            # add the movie id and the actor that acted alongside into the neighbours set
            neighbors.add((movie_id, person_id))
    return neighbors


# to run the program
if __name__ == "__main__":
    main()
