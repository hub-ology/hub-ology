from hubology import app, templated

@app.route('/inspire')
@templated()
def inspire():
    return dict()