from hubology import app, templated

@app.route('/mentors')
@templated()
def mentors():
    return dict()