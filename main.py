from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from pytube import YouTube
from fastapi import FastAPI, HTTPException
from io import BytesIO
import logging
from utils.url import is_valid_youtube_url
from data.auth import api_keys
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

# Middleware to redirect HTTP to HTTPS
app.add_middleware(HTTPSRedirectMiddleware)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class YoutubeURL(BaseModel):
    url: str

@app.get('/')
@limiter.limit("1/minute")
async def root(request: Request):
    return {'main_root' : 'Main Root', 'data': 0}

@app.post("/download_yt_audio")
@limiter.limit("20/minute")
async def download_yt_audio(youtube_url: YoutubeURL, request: Request):
    api_key = request.headers.get('Authorization')

    if api_key not in api_keys.values():
        raise HTTPException(status_code=401, detail="Unauthorized!")

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

        content_length = len(buffer.getvalue())

        return StreamingResponse(
            iter([buffer.read()]),
            media_type="audio/mpeg",
            headers={"Content-Disposition": f'filename="{title}.mp3"', "Content-Length": str(content_length),},
        )
    except Exception as e:
        logger.error(f"Failed to download audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to download audio: {str(e)}")
