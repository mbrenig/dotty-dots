from google.appengine.ext import db

class CharJson(db.Model):
    chr = db.StringProperty(multiline=False)
    json = db.TextProperty()
