from hubology import app, templated

@app.route('/developers')
@templated()
def developers():
    return dict()