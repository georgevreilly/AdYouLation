from ..AdYouLation import AdYouLation
from flask import render_template, current_app
from flask.ext.wtf import Form, TextField, RadioField, Required, Email
from gaesessions import get_current_session
import random

def create_playlist():
    videos = current_app.videos
    keys = videos["videos"].keys()
    random.shuffle(keys)
    return keys

def update_playlist():
    session = get_current_session()
    playlist = session.get('playlist')
    if not playlist:
        playlist = create_playlist()
    choices = playlist[:2]
    session['playlist'] = remaining = playlist[2:]
    return (choices, remaining)

@AdYouLation.route('/start')
def start():
    choices, remaining = update_playlist()
    return render_template("start.html", choices=choices, remaining=remaining)

class VoteForm(Form):
#   Video1Vote = RadioField(choices=("Yes!", "No!"))
#   Video2Vote = RadioField(choices=("Win!", "Lose!"))
    email = TextField('email address', [Required(), Email()])

@AdYouLation.route('/vote', methods=('GET', 'POST'))
def vote():
    form = VoteForm()
    if form.validate_on_submit():
        flash("Success")
        return redirect(url_for("start"))
    else:
        choices, remaining = update_playlist()
        return render_template("vote.html", form=form, video1=choices[0], video2=choices[1])
