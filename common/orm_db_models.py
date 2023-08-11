from common.orm_db_config import db


class SavedListing(db.Model):
    __tablename__ = 'saved_listings'
    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('sd_listings.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date_saved = db.Column(db.String)


class SDListing(db.Model):
    __tablename__ = 'sd_listings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    host_id = db.Column(db.Integer)
    host_name = db.Column(db.String)
    neighbourhood_group = db.Column(db.String)
    neighbourhood = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    room_type = db.Column(db.String)
    price = db.Column(db.Integer)
    minimum_nights = db.Column(db.Integer)
    number_of_reviews = db.Column(db.Integer)
    last_review = db.Column(db.String)
    calculated_host_listings_count = db.Column(db.Integer)
    availability_365 = db.Column(db.Integer)
    number_of_reviews_ltm = db.Column(db.Integer)
    license = db.Column(db.String)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    primaryNeighbourhood = db.Column(db.String)
