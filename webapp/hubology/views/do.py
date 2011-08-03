from hubology import app, templated

@app.route('/do')
@templated()
def do():
    return dict()