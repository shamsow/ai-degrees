from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from helper import Data

# use Data(drop=True) for faster data loading for testing purposes
data = Data(drop=True)

# Create your views here.
def index(request):
    return render(request, "brain/home.html")


def validate_name(request):
    actor1 = request.GET.get('actor1', None).lower()
    actor2 = request.GET.get('actor2', None).lower()
    valid1, valid2 = data.check_names(actor1, actor2)

    source = data.person_id_for_name(actor1)
    target = data.person_id_for_name(actor2)

    # if name returns multiple actors, format and send data
    choices = {}
    if isinstance(source, list):
        choices[actor1] = source

    if isinstance(target, list):
        choices[actor2] = target


    context = {
        'actor1_isValid': valid1,
        'actor2_isValid': valid2,
        'choices': choices,
        'id1': source,
        'id2': target
    }
    return JsonResponse(context)


def find_path(request):
    # get actor names from ajax request
    actor1 = request.GET.get('actor1', None)
    actor2 = request.GET.get('actor2', None)
    # print current task
    print("Finding path:", actor1, actor2)

    # find shortest path
    path = data.shortest_path(actor1, actor2)
    # print(path)
    # send results to page
    res = {}
    degrees = 0
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degree(s) of separation.")
        path = [(None, actor1)] + path
        for i in range(degrees):
            person1 = data.person_name_for_id(path[i][1])
            person2 = data.person_name_for_id(path[i + 1][1])

            movie = data.movie_title_for_id(path[i + 1][0])

            res[i] = {'names': [person1, person2], 'movie': movie, 'description': f"{i + 1}: {person1} and {person2} starred in {movie}"}

    print(res)
    context = {
        'path': res,
        'degrees': degrees
    }
    return JsonResponse(context)
