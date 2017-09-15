from oauth2client.client import GoogleCredentials
from google.cloud import storage
from google.gax.errors import RetryError
from slackclient import SlackClient
from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
import json, re, io, os
import pprint
import httplib2
import urllib2
from inyourface import EffectOrchestrator
import inyourface.effect
import logging

import os
app = Flask(__name__)

@app.before_first_request
def activate_job():

    global project_id, publisher, subscriber, topic_path, subscription_path, bucket_name, slack_api_token

    if (os.getenv('APPLICATION_ID')):
        project_id = os.getenv('APPLICATION_ID')
    elif (os.getenv('GCLOUD_PROJECT')):
        project_id = os.getenv('GCLOUD_PROJECT')
    elif (os.getenv('GOOLE_CLOUD_PROJECT')):
        project_id = os.getenv('GOOLE_CLOUD_PROJECT')
    elif (os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')):
        with io.open(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'), 'r', encoding='utf-8') as json_fi:
                project_id = json.load(json_fi).get('project_id')

    if (not project_id):
        return False;

    # Topics and Subscriptions
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    topic_path = publisher.topic_path(project_id, 'inyourface')
    subscription_path = subscriber.subscription_path(project_id, 'inyourface')

    # Storage
    bucket_name = os.environ.get('BUCKET_NAME')
    slack_api_token = os.environ.get("SLACK_API_TOKEN")

    # Get config.json from the default storage bucket for this project
    # You have to upload this yourself, this is a real hacky workaround for
    # there not being a good secrets solution in GAE
    if (not (bucket_name or slack_api_token)):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(project_id + ".appspot.com")
        blob = bucket.get_blob('config.json')
        config = json.loads(blob.download_as_string())
        bucket_name = config['BUCKET_NAME']
        slack_api_token = config['SLACK_API_TOKEN']


    try:
        publisher.create_topic(topic_path)
    except (RetryError) as e:
        # IGNORE: This is not, per the docs, supposed to raise an error
        print "Topic exists"

    # TODO: This is a Real Dumb Idea. This flask app should not also be acting
    # as a pub/sub worker. This should probably use GAE Task Queues, but again,
    # the GAE dev env is basically broken with flexible environment.
    try:
        subscriber.create_subscription(subscription_path, topic_path)
    except (RetryError) as e:
        # IGNORE: This is not, per the docs, supposed to raise an error.
        print "Subscription exists"

    def protected_worker(message):
        try:
            message.ack()
            if (not message_locked(message)):
                lock_message(message)
                sub_worker(message)
        except Exception as e:
            logging.exception("Exception on queue worker")


    subscriber.subscribe(subscription_path, callback=protected_worker)


def sub_worker(message):
    response_url = message.attributes.get('response_url')
    effects = message.attributes.get('effects').split(' ')
    urls = message.attributes.get('urls').split(' ')
    text = message.data

    gif = EffectOrchestrator(urls, False, False, effects)
    file_path = gif.gif()
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob_match = re.match(r".*\.([^.]+\.gif|jpg)", file_path)
    if (blob_match):
        blob = bucket.blob(blob_match.group(1))
        blob.upload_from_filename(filename=file_path)
        blob.make_public(client=client)
        os.unlink(file_path)

        req = urllib2.Request(response_url)
        req.add_header('Content-Type', 'application/json')

        response = urllib2.urlopen(req, json.dumps({
            "response_type": "in_channel",
            "text": blob.public_url
        }))

def lock_message(message):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('lock/' + message.message_id)
    blob.upload_from_string('LOCK')

def message_locked(message):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('lock/' + message.message_id)
    return blob.exists()



@app.route("/")
def hello():
    credentials = GoogleCredentials.get_application_default()
    res = credentials.authorize(httplib2.Http())
    return "Authed against google for project {}!".format(project_id)

@app.route("/slack-slash", methods = ['GET', 'POST'])
def slack():
    text = request.form['text']
    (tokens, effects, urls) = parse_slack_message(text)
    if (len(effects) == 0):
        return "You must specify some effects!"
    else:
        publisher.publish(topic_path,
            text.encode('utf-8'),
            response_url=request.form['response_url'],
            effects=' '.join(effects),
            urls=' '.join(urls)
        )

    return ":thumbsup:"

def parse_slack_message(text):
    tokens = re.split(r" +", text)
    effects = []
    urls = []
    slack_client = SlackClient(slack_api_token)
    for token in tokens:
        if (re.match(r"\+[A-Za-z]+", token)):
            effect_name = token.replace('+','')
            if (is_effect(effect_name)):
                effects.append(effect_name)
        elif (re.match(r"https?://", token)):
            urls.append(token)
        elif (re.match(r"<@U.*\|*>", token)):
            # Get user profile image
            user_lookup = slack_client.api_call('users.info', user=re.match(r"<@(U.*)\|.*>", token).group(1))
            if (user_lookup['ok']):
                for key in ("image_original","image_1024","image_512","image_192"):
                    if (key in user_lookup["user"]["profile"]):
                        urls.append(user_lookup["user"]["profile"][key])
                        break
    return (tokens, effects, urls)

def is_effect(e):
    try:
        effect_module = getattr(inyourface.effect, e[0].upper() + e[1:])
        return True
    except Exception as ex:
        return False

