from django.contrib.auth.models import User
from django.shortcuts import render
import csv, io
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from t_dist.models import Students


# Create your views here.

def home(request):
    total_std = Students.objects.all().count()

    col_std = 0
    for x in Students.objects.all():
        if x.status == 'taken':
            col_std = col_std + 1
    not_col_std = int(total_std) - int(col_std)
    position ="admin"
    if request.user.is_superuser:
        position='super'
    context = {
        'total_std': total_std,
        'col_std': col_std,
        'not_col_std': not_col_std,
        'user':request.user.username,
        'post': position
    }
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, 'home.html', context)
        else:
            return redirect("login")
    elif request.method == "POST":
        #return HttpResponse("WOW!!!!!!!!!!!!!!")
         sID = request.POST['search']
         if sID:
             std = Students.objects.filter(Q(sID__contains=sID)|Q(name__contains=sID))

             if std:
                 return render(request, "home.html", {'students': std , 'total_std': total_std,
            'col_std': col_std,
            'not_col_std': not_col_std,'user':request.user.username,'post': position})
             else:
                 return render(request, "home.html", {'msg': "No result",'total_std': total_std,
            'col_std': col_std,
            'not_col_std': not_col_std,'user':request.user.username,'post': position})
         else:
             return render(request, 'home.html', context)


def user_login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST["u_name"]
        password = request.POST["password"]
        pass1 = User.objects.get(username=username)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "login.html", {'status': 1})


def user_logout(request):
    #return HttpResponse("Kita hoise??")
    logout(request)
    return redirect("home")


def upl(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            return render(request, "upload.html",{'user':request.user.username})
        elif request.method == "POST":
            csv_file = request.FILES['std_data']
            if not csv_file.name.endswith('.csv'):
                return render(request, 'upload.html', {'status': 0,'user':request.user.username})
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                _, created = Students.objects.update_or_create(
                    sID=column[0],
                    name=column[1],
                    givenby='through_csv_file',
                    status='not_taken'
                )
        return render(request, 'upload.html', {'status': 1,'user':request.user.username})
    else:
        return redirect("home")





def add_std(request):
    if request.user.is_superuser:
        if request.method == "POST":
            name = request.POST["name"]
            sID = request.POST["sID"]
            if name == '' or sID == '':
                return render(request, "upload.html", {'msg': 'Data missing','user':request.user.username})
            else:
                student = Students.objects.filter(Q(sID__exact=sID))
                if student:
                    return render(request, "upload.html", {'msg': 'Student Already Exists','user':request.user.username})
                else:
                    n_std = Students.objects.create(name=name, sID=sID, givenby="Upload By admin", status='not_taken')
                    n_std.save()
                    return render(request, "upload.html", {'msg': 'Entry Succcessful','user':request.user.username})
    else:
        return redirect("home")







def reg(request,id):
    if request.user.is_authenticated:
        allstd = Students.objects.all().count()
        #cou = int(allstd)
        if allstd==0:
            return redirect("home")
        std=Students.objects.get(id=id)
        if std:
            std.status="taken"
            std.givenby=request.user.username
            std.save()
            total_std = Students.objects.all().count()
            position= 'admin'
            if request.user.is_superuser:
                position = 'super'
            col_std = 0
            for x in Students.objects.all():
                if x.status == 'taken':
                    col_std = col_std + 1
            not_col_std = int(total_std) - int(col_std)
            context = {
                'total_std': total_std,
                'col_std': col_std,
                'not_col_std': not_col_std,
                'user': request.user.username,
                'msg':"Entry Stroed",
                'post': position
            }

            return render(request,"home.html",context)
        else:
            return redirect("home")
    else:
        return redirect("home")


def signup(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            return render(request, "signup.html", {'user': request.user.username})
        elif request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            password2 = request.POST["password2"]
            u_level = request.POST["u_level"]
            if username == '' or password == '':
                return render(request, "signup.html", {'msg': 'Data missing', 'user': request.user.username})
            else:
                user = User.objects.filter(username=username)
                if user:
                    return render(request, "signup.html",
                                  {'msg': 'Admin Already Exists', 'user': request.user.username})
                elif password2 != password:
                    return render(request, "signup.html",
                                  {'msg': 'Password does not match', 'user': request.user.username})
                else:

                    user = User.objects.create_user(username=username,password=password)
                    if u_level =='superuser':
                        user.is_superuser = 1
                        user.is_staff = 1

                    user.save()
                    return render(request, "signup.html", {'msg': 'Entry Succcessful', 'user': request.user.username})
    else:
        return redirect("home")





def users(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            std = User.objects.all()
            return render(request, "users.html",{'students': std,'user':request.user.username})
        elif request.method == "POST":
            u_name = request.POST['search']
            if u_name:
                std = User.objects.filter(username=u_name)

                if std:
                    return render(request, "users.html", {'students': std,  'user': request.user.username})
                else:
                    return render(request, "users.html", {'msg': "No result", 'user': request.user.username})
            else:
                return render(request, 'users.html', {'user': request.user.username})
    else:
        return redirect("home")




def delete(request, id):
    if request.user.username=='fuad':
        if User.objects.all().count()==0:
            return redirect("home")
        user = User.objects.get(id=id)
        if user:
            user.delete()
        return redirect("users")
    else:
        return redirect("home")

def r_set(request,id):
    if request.user.is_superuser:
        if User.objects.all().count()==0:
            return redirect("users")
        std = User.objects.get(id=id)
        if request.method=="POST":
            pass1 = request.POST['pass1']
            pass2 = request.POST["pass2"]
            if pass1==pass2 and pass2!='':
                std.set_password(pass2)
                std.save()
                users= User.objects.all()
                return render(request,"users.html",{'students': users,'user':std.username,"msg2":"Password has been changed"})
            else:
                return render(request,"reset_pass.html",{'user':std.username,"msg2":"Password doesn't match"})
        else:
            return render(request,"reset_pass.html",{'user':std.username})
    else:
        return redirect("home")

def all_std(request):
    if request.user.is_superuser:
        if request.method=="POST":
            search = request.POST['search']
            std = Students.objects.filter(Q(name__contains=search)| Q(sID__contains=search))
            if std:
                return render(request,"all_std_data.html",{"students":std})
        else:
            std = Students.objects.all()
            return render(request, "all_std_data.html", {"students": std})
    else:
        return redirect("home")


def del_std(request, id):
    if request.user.is_superuser:
        if Students.objects.all().count()==0:
            return redirect("all_std")
        students = Students.objects.get(id=id)
        if students:
            students.delete()
        return redirect("all_std")
    else:
        return redirect("home")

def delallstd(request):
    if request.user.username=='fuad':
        Students.objects.all().delete()
    return redirect("home")

def taken(request):
    if request.user.is_superuser:
        std = Students.objects.filter(status="taken")
        col_std = 0
        for x in Students.objects.all():
            if x.status == 'taken':
                col_std = col_std + 1
        return render(request,"all_std_data.html",{"students":std,"msg55":col_std})
    else:
        return redirect("home")
