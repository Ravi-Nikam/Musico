from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="music"),
    path('signup/',views.signup,name="signup"),
    path('signIn/',views.signIn,name="signIn"),
    path('profile/',views.profile,name="profile"),
    path('Forgot_password/',views.Forgot_password,name="Forgot_password"),
    path('otp_verification/',views.otp_verification,name="otp_verification"),
    path('Change_Password/',views.Change_Password,name="Change_Password"), # for add new password
    path('New_Password/',views.New_Password,name="New_Password"), # for updating old password for user
    path('about/',views.about,name="about"),
    path('categories_genres/',views.categories_genres,name="categories_genres"),
    path('add_songs/',views.Add_audio,name="add_audio"),
    path('view_songs/',views.view_songs,name="view_song"), 
    path('logout/',views.logout,name="logout"),
    path('view_song_details/<slug:slug>',views.view_song_details,name="view_song_details"),
    path('update_song/<slug:slug>',views.update_song,name="update_song"),
    path('delete_song/<slug:slug>',views.delete_song,name="delete_song"),
    path('add_to_playlist/<slug:slug>',views.add_to_playlist,name="add_to_playlist"), # user create new playlist
    path('My_playlist',views.Your_playlist,name="My_playlist"), # user playlist 
    path('playlist_song/<int:id>',views.playlist_song,name="playlist_song"), # playlist related song
    path('remove_playlist/<int:id>',views.remove_to_playlist,name="remove_playlist"), # playlist related song
    path('add_to_existing_playlist/<int:id>/<slug:slug>',views.add_to_existing_playlist,name="add_to_existing_playlist"), # add song to existing playlist
    path('remove_from_playlist/<int:id>/<slug:slug>',views.remove_from_playlist,name="remove_from_playlist"), # remove song from playlist
] 