import datetime
from pytube import YouTube, Playlist
import os
from player import Song, p


def main(url: str, destination=r"songs"):
    l_songs = []
    if "playlist" in url.lower():
        playlist = Playlist(url)
        for video in playlist.videos:
            video = video.streams.filter(only_audio=True).first()
            out_file = video.download(output_path=destination, filename_prefix=str(datetime.datetime.now().timestamp()).split(".")[0])
            base, ext = os.path.splitext(out_file) 
            new_file =  base + '.mp3'
            try:
                os.rename(out_file, new_file) 
            except:
                os.remove(new_file)
                os.rename(out_file, new_file)
                print("overwritten File!")
            
            os.system(f"ffmpeg -i {new_file} {new_file.replace('mp3','ogg')}")
            os.remove(new_file)
            p.playlist.append(Song(filepath=new_file.replace('mp3','ogg'),name=video.title,interpret="Unknown",playing=False))
            print(video.title + " has been successfully downloaded.")



    else:
        yt = YouTube(str(url)) 
        video = yt.streams.filter(only_audio=True).first() 
        out_file = video.download(output_path=destination, filename_prefix=str(datetime.datetime.now().timestamp()).split(".")[0])
        base, ext = os.path.splitext(out_file) 
        new_file =  base + '.mp3'
        try:
            os.rename(out_file, new_file) 
        except:
            os.remove(new_file)
            os.rename(out_file, new_file)
            print("overwritten File!")

        os.system(f"ffmpeg -i {new_file} {new_file.replace('mp3','ogg')}")
        os.remove(new_file)
        p.playlist.append(Song(filepath=new_file.replace('mp3','ogg'),name=yt.title,interpret="Unknown",playing=False))
        print(yt.title + " has been successfully downloaded.")

    

