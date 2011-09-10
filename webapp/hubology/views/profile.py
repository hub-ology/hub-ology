import logging

from flaskext.login import login_required
from flaskext.login import current_user
from flask import request, redirect, url_for, current_app, flash

from hubology import app, templated, geocode_location

@app.route('/profile', methods=['GET', 'POST'])
@templated()
@login_required
def profile():
    if request.method == 'POST':
        email = request.values.get('email')
        current_user.email = email
        location_name = request.values.get('location_name')
        current_user.location_name = location_name
        location = request.values.get('location')
        logging.info(location)
        if location:
            try:
                location_parts = location[1:-1].split(',')
                current_user.set_location({'lat':float(location_parts[0]), 'lng':float(location_parts[1])})
            except:
                logging.exception("Error setting location")
                
        classification = request.values.getlist('classification')
        current_user.classification = classification
        current_user.put()
        flash('Your profile information was saved.', 'success')
        return redirect(url_for('profile'))
    else:
        return {'current_user': current_user}