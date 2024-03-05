#TODO check this
from validators import url, ValidationFailure

def is_valid_youtube_url(url: str):
    try:
        # Check if the URL is a valid URL
        if not url(url):
            return False

        # Check if the URL contains "youtube.com" or "youtu.be"
        if "youtube.com" in url or "youtu.be" in url:
            return True

        return False
    except ValidationFailure:
        return False