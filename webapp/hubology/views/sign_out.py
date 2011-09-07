from flask import redirect
from flask import session
from flask import url_for
from flaskext.login import login_required
from flaskext.login import logout_user

from hubology import app

@app.route('/sign-out')
@login_required
def sign_out():
    #Remove tokens if they're present...
    session.pop('twitter_token', None)
    session.pop('linkedin_token', None)
    session.pop('facebook_access_token', None)   
    session.pop('facebook_code', None)    
    logout_user()
    return redirect(url_for('index', _external=True))