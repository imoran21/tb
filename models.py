from django.db import models

# Create your models here.
from django.db import models
from jsonfield import JSONField
from tutorialgen import TutorialConstructor
from django.contrib.auth.models import User

def add_template():
	return TutorialConstructor().template_skeleton()



class Tutorial(models.Model):
	name = models.CharField(max_length=100, null=False)
	json_data = JSONField(null=False, default = add_template())
	password = models.CharField(max_length=40, null=False, default = "password")
	user = models.ForeignKey(User)

class PubLink(models.Model):
	name = models.CharField(max_length=20, null=False)
	tutorial = models.ForeignKey(Tutorial)
