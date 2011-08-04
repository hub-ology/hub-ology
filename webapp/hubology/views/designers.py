from hubology import app, templated

@app.route('/designers')
@templated()
def designers():
    return dict()