import requests


def download_clip(clip_url):
    """
    Uses url passed as a parameter to download a Twitch Clip

    :param clip_url: The download url of the twitch clip you wish to download
    :return: Returns the Response object of the request. This object contains the video data of the Twitch clip
    """
    index = clip_url.thumbnail_url.find('-preview')
    clip_url = clip_url.thumbnail_url[:index] + '.mp4'
    request = requests.get(clip_url)

    return request

