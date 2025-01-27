from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from .forms import CustomUserCreationForm,ProfileForm,SkillForm
from .utils import paginate_profiles, search_profile


def profiles(request):
  profiles,search_query = search_profile(request)
  custom_range,profiles = paginate_profiles(request,profiles,3)
  context = {'profiles':profiles,'search_query':search_query,'custom_range':custom_range}
  return render(request,"users/profiles.html",context)


def userProfile(request,pk):
  profile = Profile.objects.get(id=pk)
  context = {'profile':profile}
  return render(request,"users/user-profile.html",context)

def loginUser(request):
  if request.user.is_authenticated:
    return redirect('profiles')
  page = "register"
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request,"Username does not exist")
    user = authenticate(request,username=username,password=password)
    if user != None:
      login(request,user)
      return redirect('profiles')
    else:
      messages.error(request,"Username or Password is Incorrect")
  return render(request,'users/login_register.html')

def logoutUser(request):
  logout(request)
  messages.info(request,"User was logged out")
  return redirect('login')

def registerUser(request):
  page = 'register'
  form = CustomUserCreationForm()
  if request.method == "POST":
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      messages.success(request,"User Account was Created")
      login(request,user)
      return redirect('edit-account')
    else:
      messages.error(request,"An Error Occurred during registration")
  context = {'page':page,"form":form}
  return render(request,'users/login_register.html',context)


@login_required(login_url='login')
def userAccount(request):
  profile = request.user.profile

  context = {'profile':profile}
  return render(request,'users/account.html',context)


@login_required(login_url="login")
def editUser(request):
  form = ProfileForm(instance=request.user.profile)
  if request.method == "POST":
    form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
    if form.is_valid():
      form.save()
      return redirect('account')
  context = {'form' : form}
  return render(request,'users/profile_form.html',context)


@login_required(login_url="login")
def createSkill(request):
  form = SkillForm()
  if request.method == "POST":
    profile = request.user.profile
    form = SkillForm(request.POST)
    if form.is_valid():
      skill = form.save(commit=False)
      skill.owner = profile
      skill.save()
      messages.success(request,"Skill Was Added Successfully")
      return redirect('account')
  context = {'form':form}
  return render(request,'users/skill_form.html',context)


@login_required(login_url="login")
def updateSkill(request,pk):
  profile = request.user.profile
  skill = profile.skill_set.get(id=pk)
  form = SkillForm(instance=skill)
  if request.method == "POST":
    form = SkillForm(request.POST, instance=skill)
    if form.is_valid():
      skill = form.save()
      messages.success(request,"Skill Was Updated Successfully")
      return redirect('account')
  context = {'form':form}
  return render(request,'users/skill_form.html',context)

@login_required(login_url="login")
def deleteSkill(request,pk):
  profile = request.user.profile
  skill = profile.skill_set.get(id=pk)
  if request.method=="POST":
    skill.delete()
    messages.success(request,'Skill was deleted successfully')
    return redirect('account')
  context={'object':skill}
  return render(request,'delete_template.html',context)
