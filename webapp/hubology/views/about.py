from hubology import app, templated

@app.route('/about')
@templated()
def about():
    return dict()