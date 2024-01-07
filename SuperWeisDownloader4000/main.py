import os

from TwitchAPI import get_clips_by_dates, check_user, get_user_id
from quickstart import google_authenticate
from ClipsDownloader import download_clip
from GoogleAPI import upload_file, check_file_exists
from datetime import datetime
from tempfile import NamedTemporaryFile
from flask import Flask, render_template, request, redirect
from flaskwebgui import FlaskUI

app = Flask(__name__)

ui = FlaskUI(app=app, server="flask", width=500, height=500)

error_message = ""


@app.errorhandler(500)
def internal_server_error(e):
    """
    This is an error handler that runs whenever a request ends up throwing an error with status code 500
    :param e: This is an unused parameter and should be removed
    :return: Returns the html page to be rendered
    """
    global error_message
    error_message = ('''Something went wrong. \n
    try deleting the mycreds.txt file \n
    or check that the drive folder isnt full''')
    return render_template('index.html', error_message=error_message), 500


@app.route('/')
def home():
    """
    This function ensures any request made to the base URL is redirected to /index
    :return: Returns a redirect request
    """
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
async def index_page():
    """
    This function uploads Twitch clips to Google Drive if it has been reached via a POST request
    otherwise it just renders a template.
    :return: Returns the html page to be rendered
    """
    if request.method == 'POST':
        name = request.form['name']
        start_date = datetime.strptime(request.form['start'], '%Y-%m-%d')
        end_date = datetime.strptime(request.form['end'], '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        broadcaster_id = await get_user_id(name)

        google_authenticate()

        clips = await get_clips_by_dates(broadcaster_id, start_date, end_date)

        for clip in clips:

            if check_file_exists(clip.id, clip.broadcaster_name, clip.created_at.date()):
                continue

            req = download_clip(clip)

            if req.headers['Content-Type'] == 'binary/octet-stream':
                temp = NamedTemporaryFile(suffix=".mp4", delete=False)
                temp.write(req.content)
                temp.close()
                upload_file(temp.name, clip.title, clip.broadcaster_name, clip.created_at.date(), clip.id)
                os.remove(temp.name)

        return render_template('index.html', error_message=error_message)

    return render_template('index.html', error_message=error_message)


@app.route('/index/check-streamer/<name>')
async def check_streamer(name):
    """
    Checks if the streamer exists and returns the result
    :param name: Name of the streamer
    :return: Returns a JSON object containing a boolean
    """
    if request.method == 'GET':
        streamer_exists = await check_user(name.lower())
        return {"streamer_exists": streamer_exists}


if __name__ == '__main__':
    ui.run()
