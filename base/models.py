from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Room(models.Model): # model is module and Model is Class name where we are inheriting
    host = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE,null=True)
    participants = models.ManyToManyField(User,related_name='participants',blank=True) # user may join 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add = True)
    
    # using Meta use for provide metadata about class
    class Meta:
        ordering = ['-updated','-created'] # It will order like LIFO last in first out
        
    
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.body[0:50]        
    
