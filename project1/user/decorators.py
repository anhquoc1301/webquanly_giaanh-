from django.http import HttpResponse
from django.shortcuts import redirect, render
def admin_only(view_func):
    def function(request, *args, **kwargs):
        roll=request.user.roll
        if roll=='Admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("Chức năng này chỉ dành cho Admin!")
    return function
