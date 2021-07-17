from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Carmanagement
from .forms import u_r, u_r2, car_management
from .decorators import admin_only
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from .resources import Carmanagement_resources, FileExcel_Carmanagement_resources
from tablib import Dataset
# Create your views here.
class LoginClass(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request, 'new_template/signin.html')
        else:
            return redirect('user:view_camera')
    def post(self,request):
        username2 = request.POST.get('username1')
        password2= request.POST.get('password1')
        my_user = authenticate(username=username2,password=password2)
        if my_user is None:
            messages.error(request, 'Sai tài khoản hoặc mật khẩu!')
            return redirect('/')
        login(request, my_user)
        return redirect('user:view_camera')




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
        messages.success(request, 'Thêm người dùng thành công!')
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
            messages.success(request, 'Chỉnh sửa người dùng thành công!')
            return redirect('user:view_users')
        else:
            messages.error(request,'Nhập thông tin sai!')
            return redirect('/')

    return render(request, 'new_template/edit_user.html', {'bn' : form})



@admin_only
@login_required
def delete_user(request, pk):
    ur=User.objects.get(id=pk)
    if request.method=='POST':
        ur.delete()
        messages.success(request, 'Xóa người dùng thành công!')
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
    form=Carmanagement.objects.all()
    return render(request, 'new_template/vehiclemanager.html',{'form':form})



@login_required
def export_report(request):
    return render(request, 'new_template/reportsheet.html')



def logout(request):
    auth.logout(request)
    messages.success(request, 'Bạn đã đăng xuất!')
    return redirect('user:login')



@login_required
def edit_profile(request):
    ur=User.objects.get(id=request.user.id)
    form=u_r2(instance=ur)
    if request.method=="POST":
        form = u_r2(request.POST, instance=ur)
        if form.is_valid():
            form.save()
            messages.success(request, 'Chỉnh sửa thông tin thành công!')
            return redirect('user:view_camera')
        else:
            messages.error(request, 'Chỉnh sửa thất bại!')
            return redirect('/')
    return render(request, 'new_template/editprofile.html',{'form':form})



@login_required
@admin_only
def import_excel_car(request):
    if request.method=='POST':
        carmanagement_resources=Carmanagement_resources()
        dataset=Dataset()
        new_car = request.FILES.get('excel1')
        if new_car is not None:
            if not new_car.name.endswith('xlsx'):
                messages.error(request, 'Lỗi file!')
                return redirect('/')
            imported_data = dataset.load(new_car.read(), format='xlsx')
            for data in imported_data:
                # return HttpResponse({data[0]})
                value=Carmanagement(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                )
                value.save()
                messages.success(request,'Thêm thành công')
                return redirect('user:management_car')
        else:
            return redirect('user:import_excel_car')
    return render(request, 'new_template/import_carmanagement.html')



@login_required
def export_excel_cal(request):
    car_resource = Carmanagement_resources()
    dataset =car_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="car_management.xls"'
    return response



@login_required
def dowload_local_excel_car(request):
    filelocalcar_resource = FileExcel_Carmanagement_resources()
    dataset =filelocalcar_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="LocalFileImportCar.xls"'
    return response



@login_required
@admin_only
class add_managementcar(View):
    def get(self, request):
        form=car_management()
        return render(request, 'new_template/add_managementcar.html',{'form': form})
    def post(self, request):
        if request.method=="POST":
            a=car_management(request.POST, request.FILES)
            if a.is_valid():
                a.save()
                messages.success(request,'Thêm thành công')
                return redirect('user:management_car')
            else:
                messages.error(request,'Nhập sai dữ liệu')
                return redirect('/')



@login_required
@admin_only
class edit_managementcar(View):
    def get(self, request, pk):
        a=Carmanagement.objects.get(id=pk)
        form=car_management( instance=a )
        return render(request, 'new_template/edit_managementcar.html',{'form': form})
    def post(self, request, pk):
        if request.method=="POST":
            a = Carmanagement.objects.get(id=pk)
            b=car_management(request.POST,request.FILES, instance=a)
            if b.is_valid():
                b.save()
                messages.success(request,'Sửa thành công!')
                return redirect('user:management_car')
            else:
                messages.error(request, 'Nhập sai dữ liệu')
                return redirect('/')



@login_required
@admin_only
def delete_managementcar(request, pk):
        a = Carmanagement.objects.get(id=pk)
        if request.method == 'POST':
            a.delete()
            messages.success(request, 'Xóa thành công!')
            return redirect('user:management_car')
        return render(request, 'new_template/delete_managementcar.html',{'form': a})

