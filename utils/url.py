#TODO check this
from validators import url 

def is_valid_youtube_url(url_str: str):
    try:
        # Check if the URL is a valid URL
        if not url(url_str):
            return False

        # Check if the URL contains "youtube.com" or "youtu.be"
        if "youtube.com" in url_str or "youtu.be" in url_str:
            return True

        return False
    except:
        return False