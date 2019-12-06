from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render,redirect
def ourwork(request):
    return render_to_response('ourwork.html')
