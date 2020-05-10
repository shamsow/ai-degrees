# Contains the brains of the AI
# Handles the data loading and path finding
import csv
import sys

from tqdm import tqdm

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class Degree():
    # state represents the current actor
    def __init__(self, source, target, people, movies):
        self.start = source
        self.goal = target
        self.people = people
        self.movies = movies
    
    def options(self, person_id):
        movie_ids = self.people[person_id]["movies"]
        neighbors = set()
        for movie_id in movie_ids:
            for person_id in self.movies[movie_id]["stars"]:
                neighbors.add((movie_id, person_id))
        return neighbors

    def solve(self):
        # Initialize frontier to just the source actor
        start = Node(state=self.start, parent=None, action=None)
        frontier = QueueFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()
        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                # no connection so return None
                return None

            # Choose a node from the frontier
            node = frontier.remove()

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.options(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    # if the child is the goal, then return the result immediately
                    if child.state == self.goal:
                        solution = []
                        # loop and create the solution path from target to source
                        while child.parent is not None:
                            film = child.action
                            actor = child.state
                            solution.append((film, actor))
                            child = child.parent
                        # reverse the path to get from source to target
                        solution.reverse()

                        return solution
                    frontier.add(child)


# Maps names to a set of corresponding person_ids
# names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
# people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
# movies = {}

class Data():
    names = {}
    people = {}
    movies = {}
    directory = 'data/large'

    def __init__(self):
        """
        Load data from CSV files into memory.
        """
        # Load people
        with open(f"{self.directory}/people.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # print([i["name"] for i in reader])
            for row in tqdm(reader, desc="Loading people"):
                self.people[row["id"]] = {
                    "name": row["name"],
                    "birth": row["birth"],
                    "movies": set()
                }
                if row["name"].lower() not in self.names:
                    self.names[row["name"].lower()] = {row["id"]}
                else:
                    self.names[row["name"].lower()].add(row["id"])

        # Load movies
        with open(f"{self.directory}/movies.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in tqdm(reader, desc="Loading movies"):
                self.movies[row["id"]] = {
                    "title": row["title"],
                    "year": row["year"],
                    "stars": set()
                }

        # Load stars
        with open(f"{self.directory}/stars.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in tqdm(reader, desc="Loading stars"):
                try:
                    self.people[row["person_id"]]["movies"].add(row["movie_id"])
                    self.movies[row["movie_id"]]["stars"].add(row["person_id"])
                except KeyError:
                    pass


    def check_names(self, name1, name2):
        res = []
        if name1 in self.names:
            res.append(True)
        else:
            res.append(False)
        
        if name2 in self.names:
            res.append(True)
        else:
            res.append(False)

        return res


    def shortest_path(self, source, target):
        """
        Returns the shortest list of (movie_id, person_id) pairs
        that connect the source to the target.

        If no possible path, returns None.
        """

        degree = Degree(source, target, self.people, self.movies)
        path = degree.solve()
        return path


    def person_id_for_name(self, name):
        """
        Returns the IMDB id for a person's name,
        resolving ambiguities as needed.
        """
        person_ids = list(self.names.get(name.lower(), set()))
        if len(person_ids) == 0:
            return None
        # elif len(person_ids) > 1:
        #     return person_ids[0]
        #     print(f"Which '{name}'?")
        #     for person_id in person_ids:
        #         person = self.people[person_id]
        #         name = person["name"]
        #         birth = person["birth"]
        #         print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        #     try:
        #         person_id = input("Intended Person ID: ")
        #         if person_id in person_ids:
        #             return person_id
        #     except ValueError:
        #         pass
        #     return None
        else:
            return person_ids[0]
    
    def person_name_for_id(self, id):
        """
        Returns the name for a person's IMDB id
        """
        return self.people[id]["name"]
    
    def movie_title_for_id(self, id):
        return self.movies[id]["title"]
