import logging

from flaskext.login import login_required
from flaskext.login import current_user
from flask import request, redirect, url_for, current_app, flash

from hubology import app, templated
from hubology.views.sign_out import sign_out
from hubology.models import HubUser

@app.route('/delete-profile', methods=['GET'])
@login_required
def delete_profile():
    user_key = current_user.key()
    #Sign out and capture the redirect
    response = sign_out()
    #delete the user
    HubUser.delete(user_key)
    #return the redirect
    return response