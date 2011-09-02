from hubology import app, templated

from xml.etree import ElementTree
from flask import session
from flask import redirect
from flask import url_for
from flask import request
from flaskext.oauth import OAuth
import simplejson as json
import uuid
import urllib
import urllib2
import logging

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

linkedin = oauth.remote_app('linkedin',
    base_url='https://api.linkedin.com/',
    request_token_url='https://api.linkedin.com/uas/oauth/requestToken',
    access_token_url='https://api.linkedin.com/uas/oauth/accessToken',
    authorize_url='https://www.linkedin.com/uas/oauth/authorize',    
    consumer_key=app.config['LINKEDIN_CONSUMER_KEY'],
    consumer_secret=app.config['LINKEDIN_CONSUMER_SECRET']
)

facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url='https://graph.facebook.com/oauth/request_token',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    authorize_url='https://graph.facebook.com/oauth/authorize',    
    consumer_key=app.config['FACEBOOK_ID'],
    consumer_secret=app.config['FACEBOOK_SECRET']
)

        
@twitter.tokengetter
def get_twitter_token():
    return session.get('twitter_token')

@linkedin.tokengetter
def get_linkedin_token():
    return session.get('linkedin_token')

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

    
@app.route('/twitter-login', methods=['POST'])
def twitter_login():
    return twitter.authorize(callback=url_for('twitter_authorized',
        next=request.args.get('next') or request.referrer or None))

@app.route('/linkedin-login', methods=['POST'])
def linkedin_login():
    return linkedin.authorize(callback=url_for('linkedin_authorized',
        next=request.args.get('next') or request.referrer or None))

@app.route('/facebook-login', methods=['POST'])
def facebook_login():
    return redirect("https://www.facebook.com/dialog/oauth?%s" %
                    urllib.urlencode({'client_id': app.config['FACEBOOK_ID'],
                                      'redirect_uri': url_for('facebook_authorized', _external=True)}))
        
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
    session['twitter_screen_name'] = resp['screen_name']
    session['twitter_user_id'] = resp['user_id']    
    
    logging.info('You were signed in as %s' % resp['screen_name'])
    #Fetch twitter profile information
    info = twitter.get('users/show.json',
                        data={'user_id':resp['user_id']})
    if info.status == 200:        
        # logging.info(info.data)
        logging.info(info.data.get('name'))
        logging.info(info.data.get('profile_image_url'))        
        logging.info(info.data.get('location'))
        logging.info(info.data.get('url'))        
    else:
        logging.error('Unable to load profile information for twitter user: %s' % session['twitter_user'])

    return redirect(next_url)
    

@app.route('/linkedin-authorized')
@linkedin.authorized_handler
def linkedin_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        print u'You denied the request to sign in.'
        return redirect(next_url)

    logging.info(resp)

    session['linkedin_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

    #Fetch linkedin profile information
    info = linkedin.get('v1/people/~', data={})
    if info.status == 200:        
        xml = info.data
        logging.info(ElementTree.tostring(xml))
        logging.info(dir(xml))
        logging.info(xml.findtext(".//first-name"))
        logging.info(xml.findtext(".//last-name"))        

        # logging.info(info.data.get('location:(name)'))
        # logging.info(info.data.get('picture-url'))        
    else:
        logging.error('Unable to load profile information for linkedin user')

    return redirect(next_url)

@app.route('/facebook-authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    code = request.args.get('code')
    if code in (None, ''):
        #No code, send back to index page
        return redirect(url_for('index', _external=True))

    response = urllib2.urlopen("https://graph.facebook.com/oauth/access_token?%s" %
                    urllib.urlencode({'client_id': app.config['FACEBOOK_ID'],
                                  'redirect_uri': url_for('facebook_authorized', _external=True),
                                  'client_secret': app.config['FACEBOOK_SECRET'],
                                  'code':code}))
    data = response.read()
    logging.info(data)
    params = dict([part.split('=') for part in data.split('&')])
    session['facebook_access_token'] = params['access_token']
    session['facebook_code'] = code
    
    response = urllib2.urlopen("https://graph.facebook.com/me?%s" %
                    urllib.urlencode({'access_token': session['facebook_access_token']}))
    data = response.read()
    logging.info(data)
    user_info = json.loads(data)
    logging.info(user_info.get('name'))
    next_url = request.args.get('next') or url_for('index')
    
    return redirect(next_url)    
