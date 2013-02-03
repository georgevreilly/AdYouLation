from ..AdYouLation import AdYouLation
from flask import render_template, current_app, url_for, redirect
from flask.ext.wtf import Form, TextField, RadioField, Required, Email
from gaesessions import get_current_session
import random
import logging

def create_playlist():
    videos = current_app.videos
    keys = videos["videos"].keys()
    random.shuffle(keys)
    return keys

def get_choices_remaining(index=2):
    session = get_current_session()
    playlist = session.get('playlist')
    if not playlist:
        playlist = create_playlist()
    return playlist[:2], playlist[2:]

def update_playlist():
    (choices, remaining) = get_choices_remaining()
    session = get_current_session()
    session['playlist'] = remaining
    return (choices, remaining)

@AdYouLation.route('/start')
def start():
    choices, remaining = update_playlist()
    return render_template("start.html", choices=choices, remaining=remaining)

class VideoVote(RadioField):
    CHOICES = (("UP", "Yes!"), ("down", "No!"))

def vote_form(videos):
    class VoteForm(Form):
        pass

    for index, video in enumerate(videos):
        name = "video_{}".format(index+1)
        field = VideoVote(video, validators=[Required()], choices=VideoVote.CHOICES)
        setattr(VoteForm, name, field)

    return VoteForm()

@AdYouLation.route('/vote', methods=('GET', 'POST'))
def vote():
    choices, remaining = get_choices_remaining()
    form = vote_form(choices)
    if form.validate_on_submit():
        update_playlist()
        return redirect(url_for(".vote"))
    return render_template("vote.html", form=form, remaining=remaining)
