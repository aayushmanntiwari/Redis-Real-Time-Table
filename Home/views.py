import redis
from django.shortcuts import render,redirect
from rest_framework import status
from django.contrib import messages
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import *
#from .Scheduler.scheduler import download_equity,get_link
from django.conf import settings
from Home.scheduler import get_link

# Create your views here.

#need to change for production values giving by redis heroku
redis_instance = redis.StrictRedis(host='localhost',port=6379, db=0)



# Create your views here.
@api_view(['GET'])
def Home(request):
    return render(request,'index.html')




@api_view(['GET'])
def equity_request(request):
    items = {}
    key_values = []
    for key in redis_instance.keys("*"):
        if key.decode("utf-8") == 'LOW' or key.decode("utf-8") == 'HIGH' or key.decode("utf-8") == 'SC_CODE' or key.decode("utf-8") == 'OPEN' or  key.decode("utf-8") == 'SC_NAME' or   key.decode("utf-8") == 'CLOSE':
            key_values.append(key.decode("utf-8"))
    for key_value in sorted(key_values)[::-1]:
        try:
            items[key_value] = redis_instance.get(key_value).decode('utf-8').split(',')
        except:
            pass
    return JsonResponse(items,safe=False)



