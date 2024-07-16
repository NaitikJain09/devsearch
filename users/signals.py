from ssl import create_default_context
from django.db.models.signals import post_delete,post_save   
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User
   
   
def createProfile(sender,instance,created,**kwargs):
  if(created):
    user = instance
    profile = Profile.objects.create(
      user=user,
      username = user.username,
      email = user.email,
      name = user.first_name,
    )
    
def updateUser(sender,instance,created,**kwargs):
  profile = instance
  user = profile.user
  if not created:
    user.first_name = profile.name
    user.email = profile.email 
    user.username = profile.username
    user.save()
  
  
def deleteUser(sender,instance,**kwargs):
  user = instance.user
  user.delete()
  
  
# @receiver(post_delete,Profile)
post_delete.connect(deleteUser,sender=Profile)
post_save.connect(updateUser,sender=Profile)
post_save.connect(createProfile,sender=User)

