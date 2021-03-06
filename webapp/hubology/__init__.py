from flask import Flask
from flask import request, jsonify
from flask import render_template, current_app
from flaskext.login import LoginManager, current_user
from functools import wraps
import logging
import simplejson as json
import urllib
import urllib2
import uuid

from hubology.models import HubUser

def geocode_location(location_name):    
    try:
        location = None
        if location_name not in ('', None):
            response = urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?%s" %
                            urllib.urlencode({'address': location_name, 'sensor':'false'}))
            data = response.read()
            geo_info = json.loads(data)
            results = geo_info.get('results')
            if results is not None and len(results) > 0:
                geometry = results[0].get('geometry')
                if geometry is not None:
                    location = geometry.get('location')
        return location
    except:
        logging.exception("problem geocoding location")
        return None
        
        

def create_app():
    return Flask(__name__)
    
app = create_app()
app.secret_key = str(uuid.uuid4())

login_manager = LoginManager()

login_manager.setup_app(app)

@login_manager.user_loader
def load_user(userid):
    return HubUser.find(userid)

#load up some configuration settings
app.config.from_object('hubology.settings')

login_manager.login_view = "/sign-in"
login_manager.login_message = u"Please sign in to access hub-ology."

#Setup 404 handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
#Setup 500 handler
@app.errorhandler(500)
def internal_server_error(e):
    if current_user:
        from hubology.views.sign_out import sign_out
        sign_out()
    return render_template('500.html'), 500

def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator
        
@app.route('/')
@templated('index.html')
def index():
    #render the main site page
    return dict()

#Import other views
import hubology.views.about
import hubology.views.aboutlogo
import hubology.views.educators
import hubology.views.mentors
import hubology.views.developers
import hubology.views.designers
import hubology.views.inspire
import hubology.views.educate
import hubology.views.do
import hubology.views.sign_in
import hubology.views.sign_out
import hubology.views.hub
import hubology.views.map
import hubology.views.people
import hubology.views.profile
import hubology.views.delete_profile

