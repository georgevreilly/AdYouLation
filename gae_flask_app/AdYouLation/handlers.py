from ..AdYouLation import AdYouLation
from flask import render_template, current_app, url_for, redirect
from flask.ext.wtf import Form, TextField, RadioField, Required, Email
from gaesessions import get_current_session
from google.appengine.ext import db

import random
import logging
import uuid

class VideoVotes(db.Model):
    name        = db.StringProperty(required = True)
    up_votes    = db.IntegerProperty(required = True)
    down_votes  = db.IntegerProperty(required = True)

@AdYouLation.route('/_reset_votes')
def reset_votes():
    videos = current_app.videos["videos"]
    results = []
    for video in videos:
        model = VideoVotes(name=video, up_votes=0, down_votes=0)
        model.put()
    return render_template("reset_votes.html")

@AdYouLation.route('/show_votes')
def show_votes():
    results = VideoVotes.all()
    return render_template("show_votes.html", results=results)

def create_playlist():
    videos = current_app.videos
    keys = videos["videos"].keys()
    random.shuffle(keys)
    return keys

def get_choices_remaining(index=2):
    session = get_current_session()
    playlist = session.get('playlist')
    if not playlist:
        playlist = session['playlist'] = create_playlist()
    return playlist[:index], playlist[index:]

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


def vote_form(choices):
    class VoteForm(Form):
        pass

    CHOICES = (("up", "Yes!"), ("down", "No!"))
    videos = current_app.videos["videos"]

    for index, choice in enumerate(choices):
        class VideoChoice(RadioField):
            ytid = videos[choice]['ytid']

        name = "video_{}".format(index+1)
        field = VideoChoice(choice, validators=[Required()], choices=CHOICES)
        setattr(VoteForm, name, field)

    return VoteForm()

def record_vote(form):
    for index in [1, 2]:
        attrname = "video_{}".format(index)
        if hasattr(form, attrname):
            attr = getattr(form, attrname)
            name = attr.label.text
            data = attr.data
            vv = VideoVotes.gql("WHERE name = :1", name).get()
            if not vv:
                vv = VideoVotes(name=name, up_votes=0, down_votes=0)
            if data == "up":
                vv.up_votes += 1
            else:
                vv.down_votes += 1
            vv.put()

@AdYouLation.route('/vote', methods=('GET', 'POST'))
def vote():
    choices, remaining = get_choices_remaining()
    id = get_current_session()['id']
    form = vote_form(choices)
    if form.validate_on_submit():
        record_vote(form)
        update_playlist()
        return redirect(url_for(".vote"))
    else:
        return render_template("vote.html", form=form, remaining=remaining, id=id)
