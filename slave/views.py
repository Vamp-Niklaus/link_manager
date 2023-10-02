from django.shortcuts import render, redirect,HttpResponse,reverse
from datetime import datetime
from slave.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models.signals import pre_save,post_save
import math



def num(input_string):
    elements = input_string.split('&')
    numbers = [int(element) for element in elements if element]
    return numbers

def index(request):
    if request.user.is_authenticated:
        url = reverse('dir', args=["0&0&0"])
        return redirect(url)
    return redirect("signin")

def dir(request,path):
    if request.user.is_authenticated:
        us=User.objects.get(username=request.user).id
        us=Users.objects.get(user_id=us).user_id
        const=file.objects.filter(f_name="Home").filter(u_id=us).filter(p_id=None).first()
        if const is None:
            file(u_id=Users.objects.get(user_id=us),p_id=None,f_name="Home").save()
        ind=num(path)
        eid=int(ind[-2])
        eisf=int(ind[-1])
        ind=ind[:-2]
        pid=int(ind[-1])
        if(pid==0):
            pid=file.objects.get(u_id=us,p_id=None).f_id
            ind=[pid]
        path = "&".join(map(str, ind))
        file_objects = file.objects.filter(f_id__in=ind).values('f_id', 'f_name')
        z = [[file_object['f_id'], file_object['f_name']] for file_object in file_objects]
        new_list = []
        current_path = ""
        for item in z:
            current_path += str(item[0])
            new_list.append([current_path] + [item[1]])
            current_path += "&"
        context={"f":None,"l":None,"pid":pid,"path":path,"ind":new_list,"m":None,"eisf":None,"eid":None}
        fl=file.objects.filter(p_id=pid).filter(u_id=us).first()
        if fl is not None:
            obj=file.objects.filter(p_id=pid).filter(u_id=us)
            context["f"]=obj
        ll=link_list.objects.filter(u_id=us).filter(p_id=pid).first()
        if ll is not None:
            links=link_list.objects.filter(u_id=us).filter(p_id=pid)
            context["l"]=links
        mm=mc.objects.filter(u_id=us).first()
        if mm is not None:
            isf=mc.objects.get(u_id=us).isf
            isc=mc.objects.get(u_id=us).isc
            fid=mc.objects.get(u_id=us).fid

            if isf==1 and str(fid) in path:
                messages.error(request, "Can't move folder in the directory of the same folder.")
                mc.objects.filter(u_id=us).delete()
                j = path.rfind('&')
                path = path[:j]
                url = reverse('dir', args=[path+"&0&0"])
                return redirect(url)
            context["fid"]=fid
            if isf==0 and isc==0:
                context["m"]="Move Link ( "+str(link_list.objects.get(l_id=fid).name) + " ) here?"
            elif isf==0 and isc==1:
                context["m"]="Copy Link ( "+str(link_list.objects.get(l_id=fid).name)+ " ) here?"
            else :
                context["m"]="Move Folder ( "+str(file.objects.get(f_id=fid).f_name)+ " ) here?"
        if eid!=0:
            context["eisf"]=eisf
            if eisf==1:
                obj=file.objects.get(f_id=eid)
            else:
                obj=link_list.objects.get(l_id=eid)
            context["eid"]=obj
        return render(request,'a.html',context)

    return redirect("signin")


def fsave(request):
    if request.method == "POST":
        us=User.objects.get(username=request.user).id
        us=Users.objects.get(user_id=us).user_id
        name = request.POST['name']
        path = request.POST['path']
        pid = int(request.POST['pid'])
        fo_id = int(request.POST['fo_id'])

        # to not cretae folder of same same in same directory
        # obj = file.objects.filter(p_id=pid).filter(u_id=us).filter(f_name=name).first()
        # if obj is not None:
        #     messages.error(request, "Folder by this name already exist! Please try some other name.")
        #     url = reverse('dir', args=[path+"&0&0"])
        #     return redirect(url)

        if fo_id==0:
            file(u_id=Users.objects.get(user_id=us),p_id=file.objects.get(f_id=pid),f_name=name).save()
        else:
            file.objects.filter(f_id=fo_id).update(f_name=name)
        url = reverse('dir', args=[path+"&0&0"])
        return redirect(url)
    return redirect("home")

def moco(request,q):
    us=User.objects.get(username=request.user).id
    us=Users.objects.get(user_id=us).user_id
    v = q.split('*')
    path = v[0]
    isf = int(v[1])
    isc = int(v[2])
    fid = int(v[3])
    obj = mc.objects.filter(u_id=us).first()
    if obj is not None:
        mc.objects.filter(u_id=us).update(isf=isf)
        mc.objects.filter(u_id=us).update(isc=isc)
        mc.objects.filter(u_id=us).update(fid=fid)
    else:
        mc(u_id=Users.objects.get(user_id=us),isf=isf,isc=isc,fid=fid).save()
    url = reverse('dir', args=[path+"&0&0"])
    return redirect(url)


def dmoco(request,q):
    us=User.objects.get(username=request.user).id
    us=Users.objects.get(user_id=us).user_id
    if '*' in q:
        v = q.split('*')
        path = v[0]
        pid = v[1]
        isf=int(mc.objects.get(u_id=us).isf)
        isc=int(mc.objects.get(u_id=us).isc)
        fid=int(mc.objects.get(u_id=us).fid)
        if isf==0 and isc==0:
            link_list.objects.filter(l_id=fid).update(p_id=pid)
        elif isf==0 and isc==1:
            remark=link_list.objects.get(l_id=fid).remark
            name=link_list.objects.get(l_id=fid).name
            link=link_list.objects.get(l_id=fid).link
            link_list(u_id=Users.objects.get(user_id=us),remark=remark,p_id=file.objects.get(f_id=pid),link=link,name=name).save()
        else :
            file.objects.filter(f_id=fid).update(p_id=pid)
        mc.objects.filter(u_id=us).delete()
        url = reverse('dir', args=[path+"&0&0"])
        return redirect(url)
    else:
        mc.objects.filter(u_id=us).delete()
        url = reverse('dir', args=[q+"&0&0"])
        return redirect(url)



def delete(request,q):
    v = q.split('*')
    path = v[0]
    isf = int(v[1])
    fid = int(v[2])
    if isf==1:
        file.objects.filter(f_id=fid).delete()
    else:
        link_list.objects.filter(l_id=fid).delete()

    us=User.objects.get(username=request.user).id
    us=Users.objects.get(user_id=us).user_id
    ca = mc.objects.filter(u_id=us).first()
    if ca is not None:
        mc.objects.filter(u_id=us).delete()
    url = reverse('dir', args=[path+"&0&0"])
    return redirect(url)

def save(request):
    if request.method == "POST":
        us=User.objects.get(username=request.user).id
        us=Users.objects.get(user_id=us).user_id
        link = request.POST['link']
        name = request.POST['name']
        remark = request.POST['remark']
        pid = int(request.POST['pid'])
        path = request.POST['path']
        li_id = int(request.POST['li_id'])
        if li_id==0:
            link_list(u_id=Users.objects.get(user_id=us),remark=remark,p_id=file.objects.get(f_id=pid),link=link,name=name).save()
        else:
            link_list.objects.filter(l_id=li_id).update(name=name,remark=remark,link=link)
        url = reverse('dir', args=[path+"&0&0"])
        return redirect(url)
    return redirect('home')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        dob = request.POST['dob']
        gender = request.POST['gender']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        Users(id=User.objects.get(username=username).id,birthday=dob,gender=gender,user_id=User.objects.get(username=username).id).save()
        messages.success(request, "Your Account has been created succesfully!!")
        messages.success(request, "Logged In Sucessfully!!")
        user = authenticate(username=username, password=pass1)
        login(request, user)
        us=User.objects.get(username=request.user).id
        us=Users.objects.get(user_id=us).user_id
        const=file.objects.filter(f_name="Home").filter(u_id=us).filter(p_id=None).first()
        if const is None:
            file(u_id=Users.objects.get(user_id=us),p_id=None,f_name="Home").save()
        return redirect('home')

    return render(request,'signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)
        if user is not None:
            if request.user.is_authenticated:
                    logout(request)
                    messages.success(request,"Logged out sucessfully!")
            login(request, user)
            messages.success(request, "Logged In Sucessfully!!")
            return redirect('home')
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin')
    return render(request, "signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out sucessfully!")
    return render(request, "signin.html")