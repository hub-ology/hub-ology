from flaskext.login import login_required
from flaskext.login import current_user

from hubology import app, templated

@app.route('/people')
@templated()
@login_required
def people():
    return {'current_user': current_user}