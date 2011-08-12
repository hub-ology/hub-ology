from hubology import app, templated

from flask import session
from flask import redirect
from flask import url_for
from flask import request
from flaskext.oauth import OAuth
import uuid

@app.route('/sign-in')
@templated('sign-in.html')
def sign_in():
    return dict()

#Setup OAuth remote apps
oauth = OAuth()

app.secret_key = str(uuid.uuid4())

twitter = oauth.remote_app('twitter',
    base_url='http://api.twitter.com/1/',
    request_token_url='http://api.twitter.com/oauth/request_token',
    access_token_url='http://api.twitter.com/oauth/access_token',
    authorize_url='http://api.twitter.com/oauth/authenticate',    
    consumer_key=app.config['TWITTER_CONSUMER_KEY'],
    consumer_secret=app.config['TWITTER_CONSUMER_SECRET']
)
        
@twitter.tokengetter
def get_twitter_token():
    print session.get('twitter_token')
    return session.get('twitter_token')
    
@app.route('/twitter-authorized')
def twitter_authorized():
    pass
    
@app.route('/twitter-login', methods=['POST'])
def twitter_login():
    return twitter.authorize(callback=url_for('twitter_authorized',
        next=request.args.get('next') or request.referrer or None))
        
@app.route('/twitter-authorized')
@twitter.authorized_handler
def twitter_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        print u'You denied the request to sign in.'
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    print resp
    print 'You were signed in as %s' % resp['screen_name']
    return redirect(next_url)
    
