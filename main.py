from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import StreamingResponse
from pytube import YouTube
from url import is_valid_youtube_url

app = FastAPI()

@app.get('/')
async def root():
    return {'example' : 'Hello World', 'data': 0}

@app.post("/download_yt_audio")
async def download_yt_audio(url: str = Form(...)):
    if not url:
        raise HTTPException(status_code=400, detail="YouTube URL not provided!")

    if not is_valid_youtube_url(url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL!")

    try:
        yt = YouTube(url)

        audio_stream = yt.streams.filter(only_audio=True).first()

        audio_bytes = audio_stream.stream_to_buffer()

        return StreamingResponse(iter([audio_bytes]), media_type="audio/mpeg", headers={"Content-Disposition": "filename=audio.mp3"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download audio: {str(e)}")
