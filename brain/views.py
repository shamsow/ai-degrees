from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from helper import Data
data = Data()

# Create your views here.
def index(request):
    return render(request, "brain/home.html")


def validate_name(request):
    actor1 = request.GET.get('actor1', None).lower()
    actor2 = request.GET.get('actor2', None).lower()
    valid1, valid2 = data.check_names(actor1, actor2)
    context = {
        'actor1_isValid': valid1,
        'actor2_isValid': valid2
    }
    return JsonResponse(context)


def find_path(request):
    # get actor names from ajax request
    actor1 = request.GET.get('actor1', None).lower()
    actor2 = request.GET.get('actor2', None).lower()
    # print current task
    print("Finding path:", actor1, actor2)
    # get ids for actors
    source = data.person_id_for_name(actor1)
    target = data.person_id_for_name(actor2)
    # find shortest path
    path = data.shortest_path(source, target)
    
    # send results to page
    res = {}
    degrees = 0
    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degree(s) of separation.")
        path = [(None, source)] + path
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
