import re
import os
import sys
import json
import requests
import youtube_dl
from urllib.parse import parse_qs
from bs4 import BeautifulSoup

name = 'YouTubeTranscript'

class TranscriptNotFoundError(Exception):
    """
    No transcript found for the YT video.
    Please check the URL.
    """
    def __init__(self,message=None):
        if not message:
            self.message = "Please check URL. No transcript available for this URL."

    def __str__(self):
        return str(self.message)


def parse_url(vid_url):
    if 'watch?v' in vid_url:
        vid_code = re.findall(r'^[^=]+=([^&]+)', vid_url)
    elif 'youtu.be/' in vid_url:
        vid_code = re.findall(r'youtu\.be/([^&]+)', vid_url)

    else:
        raise ValueError()
    return vid_code[0]

def get_title(vid_id):
    video_info = requests.get('http://youtube.com/get_video_info?video_id=' + vid_id)
    video_info = video_info.text
    if parse_qs(video_info)['status'][0] == 'fail':
        raise TranscriptNotFoundError()
    else:
        return parse_qs(video_info)['title'][0]


def get_transcript(vid_url):
    vid_id = parse_url(vid_url)
    title = get_title(vid_id)
    if title:
        transcript = requests.get("https://www.youtube.com/api/timedtext?&v={0}&lang=en".format(vid_id))
        if "<transcript>"  not in transcript.text:
            """
            For videos that have automatically generated transcripts.
            """
            ydl_opts = {
                'skip_download':True,
                'writeautomaticsub':True,
                'subtitlesformat':'ttml',
                'quiet':True
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                result = ydl.download([vid_url])

            filename = "{0}-{1}.en.ttml".format(title,vid_id)
            try:
                with open(filename) as f:
                    transcript =[]
                    ttml = f.read()
                    soup = BeautifulSoup(ttml,'html.parser')
                    subs = soup.findAll('p')
                    for sub in subs:
                        transcript.append(sub.text)

                    os.remove(filename)
            except:
                raise TranscriptNotFoundError("No transcript for this video on YouTube.")
        else:
            """
            For videos that have manually uploaded transcripts.
            """
            soup = BeautifulSoup(transcript.text,'html.parser')
            subs = soup.findAll('text')
            transcript = []
            for sub in subs:
                text = sub.text
                text = text.replace("&quot;","")
                transcript.append(text)

        return transcript
    else:
        raise TranscriptNotFoundError()
