from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm

#extra imports for login and logout capabilities
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

def register(request):

    registered=False

    # get info from "both" forms
    if request.method == 'POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            #save User form to database
            user=user_form.save()

            # Hash the password
            user.set_password(user.password)

            # update with hashed password
            user.save()

            # now with the extra info.

            # can't commit=True because we still need to manipulate
            profile=profile_form.save(commit=False)

            # set One to One relationship between UserForm and UserPofileInfoForm
            profile.user=user

            # checking for any profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # if yes, then grab it from the POST from reply
                profile.profile_pic=request.FILES['profile_pic']

            # now save model
            profile.save()

            # registration successful
            registered=True

        else:
            print(user_form.errors,profile_form.errors)
    else:
        # was not an HTTP post so we just render the forms as blank.
        user_form=UserForm()
        profile_form=UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
                  {'user_form':user_form,
                   'profile_form':profile_form,
                   'registered':registered,

                   })

#for logins

@login_required
def special(request):
    return HttpResponse("You are logged in.")

@login_required
def user_logout(request):
    # logout the user
    logout(request)
    # return the homepage(index)
    return HttpResponseRedirect(reverse('index'))

def user_login(request):
    if request.method=='POST':
        # get username and password
        username=request.POST.get('username')
        password=request.POST.get('password')

        # django's built-in authentication function
        user=authenticate(username=username,password=password)

        # if user exists
        if user:
            # check for account active or not
            if user.is_active:
                #login the user if active
                login(request,user)
                # sending the user to the homepage(index)
                return HttpResponseRedirect(reverse('index'))
            else:
                # if account is not active
                return HttpResponse("Your account is not active")
        else:
            # if user not exists
            print("Some one tried to login and failed")
            print("They used username:{} and password:{}".format(username,password))
            return HttpResponse("Invalid  login details supplied")
    else:
        # Nothing has been provided for username and password
        return render(request,'basic_app/login.html',{})







