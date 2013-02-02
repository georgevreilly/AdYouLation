from ..AdYouLation import AdYouLation
from flask import render_template, current_app
from gaesessions import get_current_session
import random

def create_playlist():
    videos = current_app.videos
    keys = videos["videos"].keys()
    random.shuffle(keys)
    return keys

@AdYouLation.route('/start')
def start():
    session = get_current_session()
    playlist = session.get('playlist')
    if not playlist:
        playlist = create_playlist()
    choices = playlist[:2]
    session['playlist'] = remaining = playlist[2:]
 
    return render_template("start.html", choices=choices, remaining=remaining)
