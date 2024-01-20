from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import StreamingResponse
from pytube import YouTube
from fastapi import FastAPI, HTTPException
from io import BytesIO
import logging
from utils.url import is_valid_youtube_url
from pydantic import BaseModel

app = FastAPI()

# Initialize a logger
logger = logging.getLogger(__name__)

class YoutubeURL(BaseModel):
    url: str

@app.get('/')
async def root():
    return {'example' : 'Hello World', 'data': 0}

@app.post("/download_yt_audio")
async def download_yt_audio(youtube_url: YoutubeURL):
    url = youtube_url.url

    if not url:
        raise HTTPException(status_code=400, detail="YouTube URL not provided!")

    if not is_valid_youtube_url(url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL!")

    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        buffer = BytesIO()
        audio_stream.stream_to_buffer(buffer)

        buffer.seek(0)

        title = yt.title 

        return StreamingResponse(
            iter([buffer.read()]),
            media_type="audio/mpeg",
            headers={"Content-Disposition": f'filename="{title}.mp3"'},
        )
    except Exception as e:
        logger.error(f"Failed to download audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to download audio: {str(e)}")
