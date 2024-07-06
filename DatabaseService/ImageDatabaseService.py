
from flask_sqlalchemy import SQLAlchemy
class ImageDatabaseService:
    
    
    def __init__(self, db):
        self.db = db
        self.initialize()
        
    def initialize(self):
        class Image(self.db.Model):
            url = self.db.Column(self.db.String(80), primary_key=True, nullable=False)
            path = self.db.Column(self.db.String(120), unique=True, nullable=False)

        self.Image = Image

    def readAll(self):
        # read the url which is primary key, from the iamges table
        return self.Image.query.all()
    
    
    def readById(self, url):
        # read the url which is primary key, from the images table
        return self.Image.query.filter_by(url=url).first();

    def write(self, url, path):        
        image = self.Image(url=url, path=path)
        self.db.session.add(image)
        self.db.session.commit()
        
    