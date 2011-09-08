from flaskext.login import login_required
from flaskext.login import current_user

from hubology import app, templated

@app.route('/map')
@templated()
@login_required
def map():
    return {'current_user': current_user}