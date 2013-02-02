from ..AdYouLation import AdYouLation
from flask import render_template, current_app
from gaesessions import get_current_session
import random

@AdYouLation.route('/start')
def start():
    session = get_current_session()
    counter = session.get('counter', 0)
    session['counter'] =  counter + 1 
 
    videos = current_app.videos
    keys = videos["videos"].keys()
    random.shuffle(keys)
    return render_template("start.html", names=keys, counter=counter)
