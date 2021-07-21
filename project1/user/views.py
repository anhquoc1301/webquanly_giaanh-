from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Carmanagement, CarNumber
from .forms import u_r, u_r2, car_management
from .decorators import admin_only
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from .resources import Carmanagement_resources, FileExcel_Carmanagement_resources
from tablib import Dataset
from .auto import auto_download
import json
from django.core.files.storage import default_storage
import os
from .nvr_api import downloadListPlates
from datetime import datetime
import xlwt
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



@admin_only
@login_required
def add_managementcar(request):
    form=car_management()
    if request.method=="POST":
        a=car_management(request.POST, request.FILES)
        if a.is_valid():
            a.save()
            messages.success(request,'Thêm thành công')
            return redirect('user:management_car')
        else:
            messages.error(request,'Nhập sai dữ liệu')
            return redirect('/')
    return render(request, 'new_template/add_managementcar.html',{'form': form})


@admin_only
@login_required
def edit_managementcar(request, pk):
    a=Carmanagement.objects.get(id=pk)
    form=car_management(instance=a)
    if request.method=="POST":
        b=car_management(request.POST,request.FILES, instance=a)
        if b.is_valid():
            b.save()
            messages.success(request,'Sửa thành công!')
            return redirect('user:management_car')
        else:
            messages.error(request, 'Nhập sai dữ liệu')
            return redirect('/')
    return render(request, 'new_template/edit_managementcar.html',{'form': form})




@login_required
@admin_only
def delete_managementcar(request, pk):
        a = Carmanagement.objects.get(id=pk)
        if request.method == 'POST':
            a.delete()
            messages.success(request, 'Xóa thành công!')
            return redirect('user:management_car')
        return render(request, 'new_template/delete_managementcar.html',{'form': a})

auto_download()

@login_required
# k=[]
def export_report(request):
    num=CarNumber.objects.all()
    c = []
    if request.method== "POST" :
        a=request.POST.getlist('mycheck[]')
        b=request.POST.get('mydate')
        w=request.POST.get('cars')
        h=b.split('-')
        g=b.split('-')
        if h[1][0]=='0':
            h[1]=h[1].strip('0')
            h[1] = int(h[1])
        if h[2][0] == '0':
            h[2] = h[2].strip('0')
            h[2] = int(h[2])
        h[0] = int(h[0])
        h[1] = int(h[1])
        h[2] = int(h[2])
        local = 'user/media/abc'f'{g[0]}''x'f'{g[1]}''x'f'{g[2]}''/data.json'
        try:
            print("open ")
            f = default_storage.open(os.path.join(local), 'r')
            data1 = json.loads(f.read())
            for i in data1:
                    for j in a:
                        if w == 'all':
                            if i['Plate'] == j:
                                c.append(i)
                        else:
                            if i['Plate'] == j and i['Direction'] == w:
                                c.append(i)
        except:
            downloadListPlates(datetime(year=h[0], month=h[1], day=h[2]))
            f = default_storage.open(os.path.join(local), 'r')
            data1 = json.loads(f.read())
            for i in data1:
                for j in a:
                    if w =='all':
                        if i['Plate'] == j:
                            c.append(i)
                    else:
                        if i['Plate'] == j and i['Direction']==w:
                            c.append(i)

    # global k
    # k=c
    context={'form2': num, 'form': c }
    return render(request, 'new_template/reportsheet.html',context)
def export_report_excel(request):
#         global k
#         # response=HttpResponse(content_type='application/ms-excel')
#         # response['Content-Disposition']='attachment; filename=Report'+\
#         #     str(datetime.now())+'.xls'
#         # wb=xlwt.Workbook(encoding='utf-8')
#         # ws=wb.add_sheet('Report')
#         # row_num=0
#         # font_style=xlwt.XFStyle()
#         # font_style.font.bold=True
#         # columns=['Plate','Date','Time','Direction']
#         # for col_num in range(len(columns)):
#         #     ws.write(row_num, col_num,columns[col_num], font_style)
#         # font_style=xlwt.XFStyle()
#         # for row in k:
#         #     row_num+=1
#         #     for col_num in range(len(row)):
#         #         ws.write(row_num, col_num, str(row[col_num]), font_style)
#         # wb.save(response)
#         # k=[]
#         # return response
#         print({k.Time})
        return HttpResponse('s')





