from django.db import models

# Create your models here.
class Contact(models.Model):
	name=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.PositiveIntegerField()
	remarks=models.TextField()
	def __str__(self):
            return self.name

class Signup(models.Model):
	name=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.PositiveIntegerField()
	password=models.CharField(max_length=50)
	def __str__(self):
            return self.name

	
		