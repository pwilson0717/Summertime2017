from __future__ import unicode_literals
from django.db import models, IntegrityError
import bcrypt
import re


# Create your models here.
class UserManager(models.Manager):
    def registerVal(self, postData):
        results = {'status': True, 'errors': [], 'user': None}
        if not postData['name'] or len(postData['name']) < 3:
            results['status'] = False
            results['errors'].append('Please enter a valid first name')
        if not postData['alias'] or len(postData['alias']) < 3:
            results['status'] = False
            results['errors'].append('Please enter a valid alias.')
        if not postData['email'] or not re.match(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",
                postData['email']
        ):
            results['status'] = False
            results['errors'].append('Please enter a valid email')
        if not postData['birthday']:
            results['status'] = False
            results['errors'].append('Please select/enter your birthday')
        if not postData['password'] or len(postData['password']) < 8:
            results['status'] = False
            results['errors'].append('Please enter a valid password')
        if postData['password'] != postData['password2']:
            results['status'] = False
            results['errors'].append('Passwords do not match')

        if results['status']:
            try:
                user = User.objects.create(
                    name=postData['name'],
                    alias=postData['alias'],
                    email=postData['email'],
                    birthday=postData['birthday'],
                    password=(bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())))
                user.save()
                results['user'] = user
            except IntegrityError as e:
                results['status'] = False
                if 'UNIQUE constraint' in e.message:
                    results['errors'].append('That email is already registered.')
                else:
                    results['errors'].append(e.message)
        return results

    def loginVal(self, postData):
        results = {'status': True, 'user': None, 'errors': []}
        try:
            user = User.objects.get(email=postData['email'])
            if user.password == bcrypt.hashpw(postData['password'].encode(), user.password.encode()):
                pass
            else:
                raise Exception()
        except Exception as e:
            results['status'] = False
            results['errors'].append("Incorrect Username or Password")

        if results['status']:
            results['user'] = user
        return results


class User(models.Model):
    name = models.CharField(max_length=30)
    alias = models.CharField(max_length=30)
    email = models.CharField(max_length=255, unique=True)
    birthday = models.DateField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
