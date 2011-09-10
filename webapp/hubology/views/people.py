from flaskext.login import login_required
from flaskext.login import current_user

from hubology import app, templated
from hubology.models import HubUser
from paging import PagedQuery, PageLinks

PAGESIZE = 25

@app.route('/people', methods=['GET'], defaults={'page':1})
@app.route('/people/<int:page>', methods=['GET'])
@templated()
@login_required
def people(page):
    user_query = PagedQuery(HubUser.all(), PAGESIZE)
    users = user_query.fetch_page(page)
    links = PageLinks(page, user_query.page_count(), '/people/').get_links()    
    return dict(current_user=current_user, users=users, links=links, page_number=str(page))
    
@app.route('/people/json', methods=['GET'])
@templated('people.json')
@login_required
def people_json():
    """  Need to come up with a better way to get User info to client for mapping, etc.
    """
    users = HubUser.all_with_location()
    return dict(users=users)
