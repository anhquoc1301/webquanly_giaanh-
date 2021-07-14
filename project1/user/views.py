from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import User
from .forms import u_r, u_r2
from .decorators import admin_only
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import auth
# Create your views here.
class dangnhap(View):
    def get(self, request):
        return render(request, 'new_template/signin.html')
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user:view_camera')
        else:
            return redirect('user:login')

@admin_only
@login_required
def add_user(request):
    form=u_r()
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        ur=User.objects.create_user(username=username, password=password)
        ur.roll=request.POST['roll']
        ur.name = request.POST['name']
        ur.phone=request.POST['phone']
        ur.position=request.POST['position']
        ur.is_superuser=True
        ur.save()
        return redirect('user:view_users')
    return render(request,'new_template/add-user.html', {'dv' : form})

@admin_only
@login_required
def edit_user(request, pk):
    ur=User.objects.get(id=pk)
    form=u_r(instance=ur)
    if request.method=='POST':
        form=u_r(request.POST, instance=ur)
        if form.is_valid():
            form.save()
            return redirect('user:view_users')
        else:
            return HttpResponse('Thông Tin Sai, Thử Lại!')

    return render(request, 'new_template/edit_user.html', {'bn' : form})

@admin_only
@login_required
def delete_user(request, pk):
    ur=User.objects.get(id=pk)
    if request.method=='POST':
        ur.delete()
        return redirect('user:view_users')
    return render(request,'new_template/delete_user.html', {'bn' : ur })
@admin_only
@login_required
def view_users(request):
    ur=User.objects.all()
    return render(request, 'new_template/usermanager.html',{'dv':ur})
@login_required
def view_camera(request):
    return render(request, 'new_template/liveview.html')
@login_required
def management_car(request):
    return render(request, 'new_template/vehiclemanager.html')
@login_required
def export_report(request):
    return render(request, 'new_template/reportsheet.html')
def logout(request):
    auth.logout(request)
    return HttpResponse("Bạn Đã Đăng Xuất!")
@login_required
def edit_profile(request):
    ur=User.objects.get(id=request.user.id)
    form=u_r2(instance=ur)
    if request.method=="POST":
        form = u_r2(request.POST, instance=ur)
        if form.is_valid():
            form.save()
            return redirect('user:view_camera')
    return render(request, 'new_template/editprofile.html',{'form':form})
def demo(request):
    return render(request, 'new_template/liveview.html')