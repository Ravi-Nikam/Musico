from lyricsx import Lyric

# Open the .lrc file
with open("my_song.lrc") as f:
    lyric = Lyric.from_lrc(f.read())

# Extract lyrics only
lyrics = "".join(line.text for line in lyric.lines if line.is_lyric)

# Save lyrics to a text file
with open("my_song_lyrics.txt", "w") as f:
    f.write(lyrics)

# Or, to save lyrics in a Django model:
from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    lyrics = models.TextField()

# Create a new song object and set the lyrics
song = Song(title="My Song", artist="My Artist", lyrics=lyrics)
song.save()
