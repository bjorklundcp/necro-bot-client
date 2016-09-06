import json
import requests

from flask import Flask, request, flash, url_for, render_template, redirect
from wtforms import Form, StringField, validators

from necrobot import app


USER_AGENT = "NecroBot/1.0 by necrophobia155"


class AddSubredditForm(Form):
    email_address = StringField('Email Address', [
        validators.Email(message="Please enter a valid email address."),
        validators.DataRequired()
    ])
    subreddit = StringField('Subreddit', [
        validators.Length(max=20, message="Subreddits only have a max length of 20."),
        validators.DataRequired()
    ])
    key_word = StringField('Key Word', [
        validators.Length(max=120, message="Key words cannot be longer than a tweet."),
        validators.DataRequired()
    ])


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/add_subreddit', methods=['GET', 'POST'])
def add_subreddit():
    form = AddSubredditForm(request.form)
    if request.method == 'POST' and form.validate():
        email_address= form.email_address.data
        subreddit = 'https://reddit.com/r/{}/new/.json'.format(form.subreddit.data)
        key_word = form.key_word.data
        flash('Thanks for the submission')
        return redirect(url_for('index'))

    return render_template('add_subreddit.html', form=form)


def get_access_token():
    with open('secrets.json', 'r') as file:
        secrets = json.load(file)

    client_auth = requests.auth.HTTPBasicAuth(secrets.get('api_id'), secrets.get('api_secret'))
    post_data = {"grant_type": "password", "username": secrets.get('user'), "password": secrets.get('password')}
    headers = {"User-Agent": USER_AGENT}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    return response.json().get('access_token')


def get_data(endpoint, args=None):
    access_token = get_access_token()
    headers = {"Authorization": "bearer {}".format(access_token), "User-Agent": USER_AGENT}
    response = requests.get(endpoint, params=args, headers=headers)
    return response.json().get('data')

