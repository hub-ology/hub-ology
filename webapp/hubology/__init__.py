from flask import Flask
from flask import request, jsonify
from flask import render_template, current_app
from functools import wraps


def create_app():
    return Flask(__name__)
    
app = create_app()

#load up some configuration settings
app.config.from_object('hubology.default_settings')

#Setup 404 handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

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

# @app.route('/')
# @templated('splash-index.html')
# def index():
#     #render the main site page
#     return dict()

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

