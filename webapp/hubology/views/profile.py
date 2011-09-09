import logging

from flaskext.login import login_required
from flaskext.login import current_user
from flask import request, redirect, url_for, current_app, flash

from hubology import app, templated

@app.route('/profile', methods=['GET', 'POST'])
@templated()
@login_required
def profile():
    if request.method == 'POST':
        logging.info(request.values)
        email = request.values.get('email')
        current_user.email = email
        location_name = request.values.get('location_name')
        current_user.location_name = location_name
        classification = request.values.getlist('classification')
        logging.info(classification)
        current_user.classification = classification
        current_user.put()
        flash('Your profile information was saved.', 'success')
        return redirect(url_for('profile'))
    else:
        return {'current_user': current_user}