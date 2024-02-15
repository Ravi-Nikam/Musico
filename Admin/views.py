from django.shortcuts import render,redirect
from .models import User_info,genre,song,add_play_list
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.conf import settings
# from lyrics_extractor import SongLyrics  # extract lyrics from  song # lyrics_song_rv Search Engine name


# Create your views here.
def index(request):
    try:
        # <option value="2">Admin</option>
        # <option value="3">Musician</option>
        # <option value="1">User</option>
        Email_id=User_info.objects.get(Email=request.session['Email'])
        print(Email_id.User_Type)
        return render(request,'index.html',{'user_type':Email_id.User_Type})
    except Exception as e:
        print("-------------->",e)

    return render(request,'index.html')

def New_Password(request):
    if request.method == "POST" and request.POST['pwd'] == request.POST['Cpassword']:
        try:
            print(24*"*",request.session['Email'])
            user_profile=User_info.objects.get(Email=request.session['Email'])
            if user_profile:
                user_profile.Password=make_password(request.POST['pwd'])
                user_profile.save()
                del  request.session['Email']   ## after password change logout the user
                messages.success(request,"Password Successfully Changed !!")
                return redirect('signIn')
        except Exception as e:
            print("Retriving User info give some error",e)
    return render(request,'New_Password.html')

def about(request):
    return render(request,'about.html')
def signup(request):
    if request.method=="POST":
        try:
            User_info.objects.create(
                Fname=str(request.POST['Fname']).upper(),
                Lname=request.POST['Lname'],
                Dob = request.POST['Dob'],
                Gender = request.POST['Gender'],
                Email = request.POST['Mail'],
                MobileNumber = request.POST['MobileNumber'],
                Password = make_password(request.POST['Password']),
                User_Type=request.POST['User_Type'],
            )
            msg = "Successfully Registred !"
            
            return render(request,"login.html",{"msg":msg})
        except Exception as e:
            print("Something went wrong",e)
    return render(request,'signup.html')


def signIn(request):
    if request.method == "POST":
        try:
            user_mail=User_info.objects.get(Email=request.POST['Mail'])
            print("Email of user is",user_mail)
            checkpassword=check_password(request.POST['Password'],user_mail.Password)
            if checkpassword==True:
                request.session['Email']=user_mail.Email
                request.session['User_type']=user_mail.User_Type
                msg="Welcome" + user_mail.Fname
                return redirect('music')
            else:
                msg ="Please try Again !"
                return render(request,'login.html',{'msg':msg})        
        except Exception as e:
            pass
    return render(request,'login.html')


# user profile
def profile(request):
    # get the email from session
    try:
        user_profile=User_info.objects.get(Email=request.session['Email'])
    except Exception as e:
        print("Try Again !!")
    if request.method == "POST":
        user_profile.Fname= request.POST['Fname']
        user_profile.Lname= request.POST['Lname']
        user_profile.Dob = request.POST['Dob']
        user_profile.Gender= request.POST['Gender']
        user_profile.Email = request.POST['Mail']
        user_profile.MobileNumber = request.POST['MobileNumber']
        user_profile.save() 
        messages.success(request,"Profile is sucessfully updated !!")
        return render(request,'profile.html',{'user_profile':user_profile})
    return render(request,'profile.html',{'user_profile':user_profile})

def Forgot_password(request):
    if request.method=="POST":
        otp=random.randint(100000,999999) # random code ganerate 6 digit
        otp_mail=request.POST.get('Mail')
        try:
            user_email=User_info.objects.filter(Email=otp_mail).exists() # user Exist
            request.session['OTP'] = otp
            request.session['Email_OTP'] = otp_mail
            if user_email:
                subject = 'welcome to Musico world'
                message = f'Hi, thank you for registering in Musico. here is your OTP : {otp} on your email {otp_mail}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [otp_mail] # name whose want to send mail]
                value=send_mail( subject, message, email_from, recipient_list) # sent mail
            if value == 1:
                return render(request,'otp_verification.html',{'messages':"OTP sent Successfully !!"})
        except Exception as e:
            print("might wrong",e)
            return redirect('Forgot_password')
    return render(request,'forgot_password.html')

def otp_verification(request):
    try:
        otp_value=request.POST["otp"]
        if str(request.session['OTP']) == otp_value:
            del request.session['OTP'] 
            return render(request,'Change_Password.html',{'messages':messages})
        else:
            messages.warning(request,"Wrong OTP!!")
    except Exception as e:
        print("ERRROR in OTP",e)
    return redirect("/")
    
# Retrive all the Categories
        
def Change_Password(request):
    if request.method == "POST" and request.POST['pwd'] == request.POST['Cpassword']:
        try:
            print(24*"*",request.session['Email_OTP'])
            user_profile=User_info.objects.get(Email=request.session['Email_OTP'])
            if user_profile:
                user_profile.Password=make_password(request.POST['pwd'])
                user_profile.save()
                del request.session['Email_OTP']
        except Exception as e:
            print("Retriving User info give some error",e)
        
        return render(request,'Change_Password.html')


def categories_genres(request):
    
    # print(request.session['Email'])
    try:
        Email_id=User_info.objects.get(Email=request.session['Email'])
        print(Email_id.Email)
    except Exception as e:
        print("Exceptio occur",e)
        return render(request,'categories.html')
    if request.method == "POST":
        cat_music=request.POST['CategoryMusic']
        cat_des=request.POST['CategoryDescription']
        if cat_music != "" and cat_des != "":
            genre.objects.create(
                Email = Email_id,
                Name_category = request.POST['CategoryMusic'],
                Description_category = request.POST['CategoryDescription']
            )
            return render(request,'categories.html')
        messages.error(request,"Please fill out both fields")
        return render(request,'categories.html',{'Error':'Please fill out both fields'})
    else:
        return render(request,'categories.html',{'Error':'Please fill out both fields'})
        
# upload song and thair relavent info
def Add_audio(request):
    audio=genre.objects.all().values('Name_category') # fatching value category wise 
    audio_type_list=[]
    for au in audio:
        audio_type_list.append(au['Name_category'])
    try:
            song_types=request.POST.get('Song_Type')
            genre_instance, created = genre.objects.get_or_create(Name_category=song_types) # creating a instence for genre model otherwise its give error
            user_mail=User_info.objects.get(Email=request.session['Email'])
            if request.method=='POST':
                type_song=genre.objects.filter(Name_category=request.POST.get('Song_Type'))
                # file_lyrics=request.FILES['Song_Lyrics_File']
                # name,extension=str(file_lyrics).rsplit('.',1)
                # newfilename = name + '.' + 'txt'
                # print("-------------------5555555",newfilename)
                # print("*--------*******",type(file_lyrics))
                song.objects.create(
                    Email = user_mail,
                    Song_Name = request.POST['Song_Name'],
                    Song_Type = genre_instance,
                    Song_Audio_File = request.FILES['Song_Audio_File'],
                    Song_Lyrics_File  = request.FILES['Song_Lyrics_File'],
                    Song_Artist = request.POST['Song_Artist'],
                    Song_Image = request.FILES['Song_Image']
                )
            return render(request,'Add_Songs.html',context={'au':set(audio_type_list)})
    except Exception as e:
        print("ERRROR",e)
    return render(request,'Add_Songs.html',context={'au':set(audio_type_list)})


# Retrive all the songs
def view_songs(request):
    print(request.session['Email'])
    user_mail=User_info.objects.get(Email=request.session['Email'])
    try:
        if user_mail.User_Type == "2": 
            
            all_songs=song.objects.filter(Email = user_mail) # filter the user 
            print("song",all_songs)
            return render(request,'view_songs.html',{'all_song':all_songs,'user_type':user_mail.User_Type})
        elif user_mail.User_Type == "1":
            
            all_songs=song.objects.all()
            return render(request,'view_songs.html',{'all_song':all_songs,'user_type':user_mail.User_Type})
    except Exception as e:
        print("E---->",e)
    

# song with their detail view
def view_song_details(request,slug):
    try:
        all_songs=song.objects.get(slug = slug)
        return render(request,'view_song_details.html',{'all_songs':all_songs})
    except Exception as e:
        print("ERROR IN VIEW DETAILS ",e)
    return render(request,'view_song_details.html')



# update the song related information 
def update_song(request,slug):
    try:
        song_updation=song.objects.get(slug=slug) # verify slug and retriving song instance
        list_cate=genre.objects.all().values() # fatch all the genre list 
        audio_type_list=[]
        for au in list_cate:
            audio_type_list.append(au['Name_category'])
        try:
            song_types=request.POST.get('Song_Type')
            genre_instance, created = genre.objects.get_or_create(Name_category=song_types) # Retrive the object of song which is manytomany
        except Exception as e:
            pass    
        if request.method == 'POST':
            song_updation.Song_Name = request.POST['Song_Name']
            song_updation.Song_Type = genre_instance
            try: 
                song_updation.Song_Audio_File = request.FILES['Song_Audio_File'] # for handling any audio file related Exception
            except KeyError:
                pass
            song_updation.Song_Artist = request.POST['Song_Artist'] 
            try:
                song_updation.Song_Image = request.FILES['Song_Image'] # for handling any file related Exception
            except KeyError:
                pass
            
            song_updation.save()
            msg = "Successfully"
            # return render(request,'view_songs.html',{'song_information':song_updation,'list_category':audio_type_list,"msg":msg})
            return redirect('view_song')
    except Exception as e:
        print("update song error",e) # More informative error message
    return render(request,'Update_song.html',{'song_information':song_updation,'list_category':list_cate})

def delete_song(request,slug):
    song_updation=song.objects.get(slug=slug)
    song_updation.delete()
    return redirect('view_song')


# list of user created playlist
def Your_playlist(request): 
    try:
        list_of_playlist=add_play_list.objects.filter(Email=request.session['Email'])
        return render(request,'your_playlist.html',{'list_of_playlist':list_of_playlist})
    except Exception as e:
        print("Error Retriving Playlist",e) # More informative error message
        return redirect("/")


# user wise playlist song (Detail view of playlist)
def playlist_song(request,id):
    try:
        song_list=add_play_list.objects.get(id=id)
        print(song_list)
        return render(request,'playlist_song.html',{'all_song':song_list})
    except Exception as e:
        print("Playlist Song Retriving Error ",e) # More informative error message
    return render(request,'playlist_song.html')

# Create New Playlist
def add_to_playlist(request,slug):
    Play_list=add_play_list.objects.filter(Email=request.session['Email']) # filter the playlist as per user
    song_updation=song.objects.get(slug=slug) # Retrive the song for add to playlist and for display purpose
    if request.method == "POST":
        try:
            user_mail=User_info.objects.get(Email=request.session['Email'])
            play_lst=add_play_list.objects.create(
                Email = user_mail,
                PlayList_Name=request.POST['playlist'],
            )
            play_lst.Songs.set([song_updation]) # Use .set() to assign directly for ManyToMany relationship
            return redirect('view_song')    
        except Exception as e:
            print("Error in playtlist",e) # More informative error message
        return redirect('view_song')
    return render(request,'add_playlist.html',{'Play_list':Play_list,"song_updation":song_updation})
    

# discard playlist form the table
def remove_to_playlist(request,id):
    try:
        playlist=add_play_list.objects.get(id=id) # retrive the playlist instance
        playlist.delete() # delete the playlist
        messages.success(request,"Successfully Playlist Removed !!") 
        return redirect('My_playlist')
    except Exception as e:
        messages.success(request,"Error during discarding Playlist !! Please try again !! ")
        return redirect('My_playlist')
        

# Add Song to existing Playlist
def add_to_existing_playlist(request,id,slug):
    try:

        playlist=add_play_list.objects.get(id=id)         #  retrieve the playlist instance as needed ...
        try:
            song_of_playlist=song.objects.get(slug=slug) #   retrieve the song instance as needed ...
            playlist.Songs.add(song_of_playlist)         #   add song instance to playlist
            playlist.save()                              # Save changes to the database
            messages.success(request,"Song added to playlist successfully!")
        except Exception as e:
            print("Error retrieving song:", e)            # More informative error message
            messages.error(request, "Error adding song to playlist. Please try again.")

    except Exception as e:
        print("Existing play list error",e)
        messages.error(request, "Error accessing playlist. Please try again.")
    return redirect('view_song') # Redirect to the view_song view


# Remove song from the Playlist
def remove_from_playlist(request,id,slug):
    try:
        playlist=add_play_list.objects.get(id=id)         #  retrieve the playlist instance as needed ...
        try:
            song_of_playlist=song.objects.get(slug=slug) #   retrieve the song instance as needed ...
            playlist.Songs.remove(song_of_playlist)         #   add song instance to playlist
            messages.success(request,"Song discarded to playlist successfully!")
        except Exception as e:
            print("Error retrieving song:", e)  # More informative error message
            messages.error(request, "Error removing song to playlist. Please try again.")

    except Exception as e:
        print("Existing play list error",e)
        messages.error(request, "Error accessing playlist. Please try again.")
    return redirect('view_song') # Redirect to the view_song view

def logout(request):
    del request.session['Email']
    del request.session['User_type']
    return redirect('/')

