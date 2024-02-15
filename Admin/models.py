from django.db import models
from django.utils import timezone
# from django.core.validators import 
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.crypto import get_random_string
# from os import rename
import os

# Create your models here.
class User_info(models.Model):
    Fname= models.CharField(max_length=100)
    Lname= models.CharField(max_length=100)
    Dob = models.CharField(max_length=100)
    Gender= models.CharField(max_length=10)
    Email = models.EmailField(max_length=100,primary_key=True)
    MobileNumber = models.PositiveBigIntegerField()
    Password = models.CharField(max_length=100)
    User_Type= models.CharField(max_length=100)

    def clean(self):
        if self.Dob > timezone.now().date():
            raise ValidationError("Date of Birth cannot be in the future.")
        return 

    def __str__(self):
        return self.Email 
    
class genre(models.Model):
    Email = models.ForeignKey(User_info,on_delete=models.CASCADE)
    Name_category = models.CharField(max_length=50,unique=True)
    Description_category = models.CharField(max_length=100,default="Other")
    Created = models.DateField(auto_now=False, auto_now_add=True) # store current date
    updated = models.DateField(auto_now=True,auto_now_add=False) # store  Last Updated date

    def __str__(self):
        return self.Name_category

    

def custom_slug(name,artist):
    custom_string = name + artist + " " + get_random_string(length=8) 
    
    slug = slugify(custom_string)

    while song.objects.filter(slug=slug).exists():
        slug = slugify(custom_string) + get_random_string(length=4)

    return slug

# for convert file from lrc to txt
# def modify_lyr_name(file):
#     print("FILE NAMe is ",type(file))
#     name,extension=str(file).rsplit('.',1)
#     print("NAME OF THE FILE IS",name)
#     newfilename = name + '.' + 'txt'
#     # file_name,extenstion=os.path.splitext(file.name)
#     # new_file_name = f"{file_name}.txt"
#     field=song._meta.get_field('Song_Lyrics_File').upload_to
#     # x=os.path.join(field.,newfilename)
#     print("***********************>>>>",x)
#     # os.rename(file,x)

class song(models.Model):
    Email = models.ForeignKey(User_info,on_delete=models.CASCADE)
    Song_Name = models.CharField(max_length=100)
    Song_Type = models.ForeignKey(genre,on_delete=models.CASCADE,related_name="genres")
    Song_Audio_File = models.FileField(upload_to='songs/')
    Song_Lyrics_File = models.FileField(upload_to='songs_Lyrics/',default="Not Avaliable")
    Song_Artist = models.CharField(max_length=50)
    Song_Image = models.ImageField(upload_to='Song_image/')
    Song_Created = models.DateField(auto_now=False, auto_now_add=True) # store current date
    Song_updated = models.DateField(auto_now=True,auto_now_add=False)
    slug = models.SlugField(unique=True)

    

    @property
    def modified_name(self):
        return self.Song_Name.replace(' ', '_')
    

    
    
    def save(self,*args,**kwargs):
        # modify_lyr_name(self.Song_Lyrics_File.path) # calling converting file function
        self.slug = custom_slug(self.Song_Name,self.Song_Artist)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.Song_Artist
    
    
    class Meta:
        verbose_name_plural = 'Songs'  # Specify the plural form of the model name


class add_play_list(models.Model):
    Email = models.ForeignKey(User_info,on_delete=models.CASCADE)
    Songs = models.ManyToManyField(song, related_name='playlists')  
    PlayList_Name = models.CharField(max_length=20,default="My_Playlist")
    Song_Created = models.DateField(auto_now=False, auto_now_add=True) # store current date

    
    def __str__(self):
        return self.PlayList_Name