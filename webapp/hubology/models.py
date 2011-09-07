#Please keep the google appengine specific imports limited to this 
#module. (To help with refactoring if we switch to another hosting solution)
from google.appengine.ext import db

import logging

#These models may end up switching up to http://mongoalchemy.org/
#(or something similar) if hub-ology.org moves off of AppEngine

class HubUser(db.Model):
    socnet = db.StringProperty(required=True, choices=set(["twitter", "facebook", "linkedin"]))
    userid = db.StringProperty(required=True)
    hubid = db.StringProperty(required=True)    
    username = db.StringProperty()
    name = db.StringProperty(required=True)
    location = db.GeoPtProperty() #Lat/Lng from browser/device
    location_name = db.StringProperty()
    town = db.StringProperty()  #Name of town where they live/want to support
    email = db.StringProperty()
    link = db.StringProperty()
    url = db.StringProperty() 
    gender = db.StringProperty()
    profile_image_url = db.StringProperty()       
    #list of mentor, educator, developer, designer
    classification = db.StringListProperty()
    original_insert_date = db.DateTimeProperty(auto_now_add=True)
    last_modified_date = db.DateTimeProperty(auto_now=True)    
        
    def is_authenticated(self):
        """ Is this user authenticated?
            We'll just say True for now.
            If we've got a HubUser object, they had to 
            come from Twitter, Facebook, or LinkedIn
        """
        return True
        
    def is_active(self):
        """ Is this an active user?
            For now, all users are considered 'Active'
        """
        return True       
        
    def is_anonymous(self):
        """ Is this an anonymous user?
            No HubUsers are anonymous so it's always False
        """ 
        return False
        
    def get_id(self):
        return self.hubid
    
    @staticmethod
    def find(hubid):
        
        if hubid in ('', None):
            return None
        
        user = db.GqlQuery("""SELECT * FROM HubUser
                               WHERE hubid = :1
                            """, hubid).get()
        return user