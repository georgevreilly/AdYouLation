from ..AdYouLation import AdYouLation
from flask import render_template, current_app

@AdYouLation.route('/start')
def start():
    videos = current_app.videos
    keys = videos["videos"].keys()
    return render_template("start.html", names=keys)
