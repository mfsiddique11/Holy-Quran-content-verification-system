from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render,redirect
def developers(request):
    return render_to_response('developers.html')
