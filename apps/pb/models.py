from __future__ import unicode_literals
from django.db import models, IntegrityError
from ..login.models import User


class PokeManager(models.Manager):
    def addPoke(self, postData, session_id):
        results = {'status': True, 'errors': []}
        if not postData['submit']:
            results['status'] = False
            results['errors'].append('You must use the button to poke')
        if not postData['submit'].isdigit():
            results['status'] = False
            results['errors'].append('Whoa! try again!')

        try:
            user = User.objects.get(id=session_id)
            gettingPoked = User.objects.get(id=int(postData['submit']))

            poke = Poke.objects.create(poker=user, pokee=gettingPoked)
            poke.save()

        except IntegrityError as e:
            results['status'] = False
            results['errors'].append(e.message)

        return results


# Create your models here.
class Poke(models.Model):
    poker = models.ForeignKey('login.User', related_name='poked', null=True)
    pokee = models.ForeignKey('login.User', related_name='gotPoked', null=True)

    objects = PokeManager()

