from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def dashboard(request):
    user_in_session = User.objects.get(
        email=request.session['email_session_id'])
    context = {
        'user_wishes': Wish.objects.filter(user=user_in_session, wish_granted=False),
        'user': user_in_session,
        'granted_wishes': Wish.objects.filter(wish_granted=True)

    }
    return render(request, 'dashboard.html', context)


def create(request):
    user_in_session = User.objects.get(
        email=request.session['email_session_id'])
    context = {
        'user': user_in_session
    }
    return render(request, 'create.html', context)


def editwish(request, wish_id):
    user_in_session = User.objects.get(
        email=request.session['email_session_id'])
    context = {
        'wish': Wish.objects.get(id=wish_id),
        'user': user_in_session
    }
    return render(request, 'editwish.html', context)


def stats(request):
    user = User.objects.get(email=request.session['email_session_id'])
    context = {
        'user': user,
        'total_wishes_granted': Wish.objects.filter(wish_granted=True),
        'pending_wishes': Wish.objects.filter(wish_granted=False, user=user),
        'granted_wishes': Wish.objects.filter(wish_granted=True, user=user),
    }
    return render(request, 'stats.html', context)

#
#
#
#
# redirect functions------
#
#
#
#

def register(request):
    user_errors = User.objects.user_validator(request.POST)
    if len(user_errors) > 0:
        for key, value in user_errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hashed_pw = bcrypt.hashpw(
            request.POST["password"].encode(), bcrypt.gensalt()).decode()
    print("hashed_pw:", hashed_pw)
    new_user = User.objects.create(
        first_name=request.POST["first_name"],
        last_name=request.POST["last_name"],
        email=request.POST["email"],
        password=hashed_pw
    )
    request.session["email_session_id"] = new_user.email
    return redirect('/wishes')

def login(request):
    user_list = User.objects.filter(email=request.POST["email"])
    if len(user_list) == 1:
        print("We found User")
        print(user_list[0].password)
        print(request.POST)
        if bcrypt.checkpw(request.POST["password"].encode(), user_list[0].password.encode()):
            print("password match")
            request.session["email_session_id"] = user_list[0].email
            return redirect("/wishes")
        else:
            print("password failed")
            messages.error(request, "password failed")
            return redirect("/")
    else:
        print("no user with that email")
        messages.error(request, "no user with that email")
        return redirect('/')


def logout(request):
    request.session.clear()

    return redirect('/')


def create_wish(request):
    wish_errors = Wish.objects.wish_validator(request.POST)
    if len(wish_errors) > 0:
        for key, value in wish_errors.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    else:
        Wish.objects.create(
            wish_name=request.POST['wish_name'],
            wish_description=request.POST['wish_description'],
            user=User.objects.get(email=request.session['email_session_id'])
        )
    return redirect('/wishes')


def edit(request, wish_id):
    wish_errors = Wish.objects.wish_validator(request.POST)
    if len(wish_errors) > 0:
        for key, value in wish_errors.items():
            messages.error(request, value)
        return redirect(f'/wishes/edit/{wish_id}')
    else:
        wish_to_edit = Wish.objects.get(id=wish_id)
        wish_to_edit.wish_name = request.POST['wish_name']
        wish_to_edit.wish_description = request.POST['wish_description']
        wish_to_edit.save()

    return redirect('/wishes')


def delete(request, wish_id):
    wish_to_delete = Wish.objects.get(id=wish_id)
    wish_to_delete.delete()
    return redirect('/wishes')


def granted_wish(request, wish_id):
    batmans_idea = Wish.objects.get(id=wish_id)
    batmans_idea.wish_granted = True
    batmans_idea.save()

    return redirect('/wishes')


def like_wish(request, wish_id):
    user = User.objects.get(
        email=request.session["email_session_id"])
    wish_to_like = Wish.objects.get(id=wish_id)
    wish_to_like.users_who_liked.add(user)
    return redirect('/wishes')