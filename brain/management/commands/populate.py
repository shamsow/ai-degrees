# Load data from csv into Models
import csv
import sys
from tqdm import tqdm
from django.core.management.base import BaseCommand, CommandError

from brain.models import Actor, Movie
# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

# def load_data(directory):
#     """
#     Load data from CSV files into Models.
#     """
#     # Load people
#     with open(f"{directory}/people.csv", encoding="utf-8") as f:
#         reader = csv.DictReader(f)
#         # print([i["name"] for i in reader])
#         for row in tqdm(reader, desc="Loading people"):
#             # people[row["id"]] = {
#             #     "name": row["name"],
#             #     "birth": row["birth"],
#             #     "movies": set()
#             # }
#             # if row["name"].lower() not in names:
#             #     names[row["name"].lower()] = {row["id"]}
#             # else:
#             #     names[row["name"].lower()].add(row["id"])
            
#             person = Actor(imdb=row["id"], name=row["name"].lower(), birth=row["birth"])
#             person.save()

class Command(BaseCommand):
    help = "Populate the apps models with the actor and movie data from the csv files"
    
    def add_arguments(self, parser):
        parser.add_argument('directory', nargs='+', type=str)
    
    def handle(self, *args, **options):
        # Load people
        directory = options['directory'][0]

        with open(f"{directory}/people.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            objects = []
            for row in tqdm(reader, desc="Loading people"):
                if Actor.objects.filter(imdb=row["id"]).exists():
                    continue
                birth = row["name"]
                try:
                    birth = int(birth)
                except:
                    birth = 0

                person = Actor(imdb=row["id"], name=row["name"].lower(), birth=birth)
                objects.append(person)
            Actor.objects.bulk_create(objects)


        # Load movies
        # with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        #     reader = csv.DictReader(f)
        #     for row in tqdm(reader, desc="Loading movies"):
        #         movies[row["id"]] = {
        #             "title": row["title"],
        #             "year": row["year"],
        #             "stars": set()
        #         }
                
        #         film = Movie(imdb=row["id"], title=row["title"], year=row['year'])
        #         film.save()
        # Load stars
        # with open(f"{directory}/stars.csv", encoding="utf-8") as f:
            # reader = csv.DictReader(f)
            # for row in tqdm(reader, desc="Loading stars"):
            #     try:
            #         people[row["person_id"]]["movies"].add(row["movie_id"])
            #         movies[row["movie_id"]]["stars"].add(row["person_id"])
            #     except KeyError:
            #         pass

# def person_id_for_name(name):
#     """
#     Returns the IMDB id for a person's name,
#     resolving ambiguities as needed.
#     """
#     person_ids = list(names.get(name.lower(), set()))
#     if len(person_ids) == 0:
#         return None
#     elif len(person_ids) > 1:
#         print(f"Which '{name}'?")
#         for person_id in person_ids:
#             person = people[person_id]
#             name = person["name"]
#             birth = person["birth"]
#             print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
#         try:
#             person_id = input("Intended Person ID: ")
#             if person_id in person_ids:
#                 return person_id
#         except ValueError:
#             pass
#         return None
#     else:
#         return person_ids[0]

# def main():
#     if len(sys.argv) > 2:
#         sys.exit("Usage: python3 degrees.py [directory]")
#     directory = sys.argv[1] if len(sys.argv) == 2 else "small"

#     # Load data from files into memory
#     print("Loading data...")
#     load_data(directory)
#     print("Data loaded.")
    # print(movies)

    # source = person_id_for_name(input("Name: "))
    # # print(source)
    # if source is None:
    #     sys.exit("Person not found.")
    # target = person_id_for_name(input("Name: "))
    # # print(target)
    # if target is None:
    #     sys.exit("Person not found.")

    # path = shortest_path(source, target)
    # if path is None:
    #     print("Not connected.")
    # else:
    #     degrees = len(path)
    #     print(f"{degrees} degree(s) of separation.")
    #     path = [(None, source)] + path
    #     for i in range(degrees):
    #         person1 = people[path[i][1]]["name"]
    #         person2 = people[path[i + 1][1]]["name"]
    #         movie = movies[path[i + 1][0]]["title"]
    #         print(f"{i + 1}: {person1} and {person2} starred in {movie}")

# if __name__ == "__main__":
#     main()