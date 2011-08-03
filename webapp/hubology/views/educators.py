from hubology import app, templated

@app.route('/educators')
@templated()
def educators():
    return dict()