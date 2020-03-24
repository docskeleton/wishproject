from django.db import models
from django.contrib import messages
import re


# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, post_data):
        user_errors = {}
        if len(post_data["first_name"]) < 3:
            user_errors["first_name"] = "first name should be at least 3 characters"
        if len(post_data["last_name"]) < 3:
            user_errors["last_name"] = "last name should be at least 3 characters"
        Email_Regex = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not Email_Regex.match(post_data['email']):
            user_errors['email'] = 'invalid email address!'
        if len(post_data["email"]) < 3:
            user_errors["email"] = "email should be at least 3 characters"
        if len(post_data["password"]) < 3:
            user_errors["password"] = "password should be at least 3 characters"
        if post_data["password_confirm"] != post_data['password']:
            user_errors["password_confirm"] = "passwords do not match"
        return user_errors

class WishManager(models.Manager):
    def wish_validator(self, post_data):
        wish_errors = {}
        if len(post_data["wish_name"]) < 3:
            wish_errors["wish_name"] = "wish should be at least 3 characters"
        if len(post_data["wish_description"]) < 3:
            wish_errors["wish_description"] = "wish description should be at least 3 characters"
        return wish_errors

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Wish(models.Model):
    wish_name = models.CharField(max_length=30)
    wish_description = models.TextField()
    wish_granted = models.BooleanField(default=False)
    user = models.ForeignKey(
        "User", related_name="user_wishes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()
    users_who_liked = models.ManyToManyField("User", related_name="liked_wish")

