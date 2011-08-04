from hubology import app, templated

@app.route('/about-logo')
@templated('about-logo.html')
def about_logo():
    return dict()