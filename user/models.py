from django.db import models

# Create your models here.
class userModel(models.Model):
    name = models.TextField(null=False)
    email = models.EmailField(null=False)
    password = models.TextField(null=False)
    data = models.TextField(null=False)
    img = models.ImageField(upload_to="profile", null=False)
    isLoged = models.TextField(default="False", null=False)
    firebaseId = models.TextField(null=False)
    contacts = models.TextField(null=False)
    
    