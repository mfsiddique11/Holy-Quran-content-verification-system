from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render,redirect
def references(request):
    return render_to_response('references.html')
