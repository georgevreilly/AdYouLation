from ..AdYouLation import AdYouLation
from flask import render_template, current_app, url_for, redirect
from flask.ext.wtf import Form, TextField, RadioField, Required, Email
from gaesessions import get_current_session
from google.appengine.ext import db

import random
import logging
import uuid

class Video(db.Model):
    name        = db.StringProperty(required = True)
    up_votes    = db.IntegerProperty(required = True)
    down_votes  = db.IntegerProperty(required = True)

@AdYouLation.route('/_reset_votes')
def reset_votes():
    videos = current_app.videos["videos"]
    results = []
    for video in videos:
        model = Video(name=video, up_votes=0, down_votes=0)
        model.put()
    return render_template("reset_votes.html")

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
    get_current_session()['playlist'] = remaining
    return (choices, remaining)

@AdYouLation.route('/start')
def start():
    session = get_current_session()
    session['playlist'] = create_playlist()
    if not session.get('id'):
        session['id'] = uuid.uuid4()
    return render_template("start.html")

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
    id = get_current_session()['id']
    form = vote_form(choices)
    if form.validate_on_submit():
        update_playlist()
        return redirect(url_for(".vote"))
    return render_template("vote.html", form=form, remaining=remaining, id=id)
