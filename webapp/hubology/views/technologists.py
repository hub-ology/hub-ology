from hubology import app, templated

@app.route('/technologists')
@templated()
def technologists():
    return dict()