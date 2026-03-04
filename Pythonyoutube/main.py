import yt_dlp

url = "https://www.youtube.com/shorts/LXCtAykJ3Tw"
ydl_opts={
    'outtmpl':'videolar/%(title)s.%(ext)s'
}
with yt_dlp.YoutubeDL() as ydl:
    ydl.download([url])