from hubology import app, templated

from xml.etree import ElementTree
from flask import session
from flask import redirect
from flask import url_for
from flask import request
from flaskext.oauth import OAuth
from flaskext.login import login_user
import simplejson as json
import urllib
import urllib2
import logging

from hubology.models import HubUser

@app.route('/sign-in')
@templated('sign-in.html')
def sign_in():
    return dict()

#Setup OAuth remote apps
oauth = OAuth()

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

#This code was written prior to flask-oauth being updated 
#to support Facebook.  Need to revisit this and sync with the 
#new flask-oauth changes.
#  https://github.com/mitsuhiko/flask-oauth
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
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

    #Fetch twitter profile information
    info = twitter.get('users/show.json',
                        data={'user_id':resp['user_id']})
    if info.status == 200:        
        hubid = u'twitter-%s' % resp['user_id']

        user = HubUser.find(hubid)
        if user is None:
            #This is the first time this twitter user has signed in
            #to hub-ology.  We'll need to create a new HubUser for them.
            user = HubUser(socnet=u'twitter', userid=resp['user_id'],
                           hubid=hubid, name=info.data.get('name'))

            user.profile_image_url = info.data.get('profile_image_url')
            user.location_name = info.data.get('location')
            user.url = info.data.get('url')
            user.username = resp['screen_name']
            user.link = u'https://twitter.com/#!/%s' % resp['screen_name']
            
            #Save the user
            user.put()
        
        login_user(user)
        #Redirect the user to the 'hub'
        return redirect(url_for('hub', _external=True))
    else:
        logging.error('Unable to load profile information for twitter user: %s' % session['twitter_user'])
        return redirect(url_for('sign_in', _external=True))
    

@app.route('/linkedin-authorized')
@linkedin.authorized_handler
def linkedin_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        return redirect(next_url)


    session['linkedin_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

    #Fetch linkedin profile information
    info = linkedin.get('v1/people/~:(id,first-name,last-name,public-profile-url,picture-url)', data={})
    if info.status == 200:        
        xml = info.data
        # logging.info(ElementTree.tostring(xml))
        linkedin_id = xml.findtext(".//id")
        name = u'%s %s' % (xml.findtext(".//first-name"), xml.findtext(".//last-name"))
        link = u'%s' % xml.findtext(".//public-profile-url")
        profile_image_url = u'%s' % xml.findtext(".//picture-url")                
        hubid = u'linkedin-%s' % linkedin_id

        user = HubUser.find(hubid)
        if user is None:
            #This is the first time this LinkedIn user has signed in
            #to hub-ology.  We'll need to create a new HubUser for them.
            user = HubUser(socnet=u'linkedin', userid=linkedin_id,
                           hubid=hubid, name=name)

            user.profile_image_url = profile_image_url
            user.link = link
            
            #Save the user
            user.put()
        
        login_user(user)
        #Redirect the user to the 'hub'
        return redirect(url_for('hub', _external=True))
        
    else:
        logging.error('Unable to load profile information for linkedin user')
        return redirect(next_url)

@app.route('/facebook-authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
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
    params = dict([part.split('=') for part in data.split('&')])
    session['facebook_access_token'] = params['access_token']
    session['facebook_code'] = code
    
    response = urllib2.urlopen("https://graph.facebook.com/me?%s" %
                    urllib.urlencode({'access_token': session['facebook_access_token']}))
    data = response.read()
    user_info = json.loads(data)
    logging.info(user_info.get('name'))

    facebook_id = user_info.get('id')
    hubid = u'facebook-%s' % facebook_id

    user = HubUser.find(hubid)
    if user is None:
        #This is the first time this Facebook user has signed in
        #to hub-ology.  We'll need to create a new HubUser for them.
        user = HubUser(socnet=u'facebook', userid=facebook_id,
                       hubid=hubid, name=user_info.get('name'))

        user.username = user_info.get('username')
        user.profile_image_url = u'https://graph.facebook.com/%s/picture' % user_info.get('username')
        user.link = user_info.get('link')
        user.gender = user_info.get('gender')
        
        #Save the user
        user.put()
    
    login_user(user)
    #Redirect the user to the 'hub'
    return redirect(url_for('hub', _external=True))
    