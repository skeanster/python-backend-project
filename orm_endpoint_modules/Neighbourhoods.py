from flask_restful import Resource
from flask import jsonify, request, Blueprint
from common.orm_db_config import db
from common.orm_db_models import SDListing
from common.orm_common_functions import row2dict

bp = Blueprint('views', __name__)


class Neighbourhoods(Resource):
    def get(self):
        result = []
        location = request.args.get("location")

        if location:
            listings = SDListing.query.filter_by(neighbourhood=location).all()

            result = [row2dict(listing) for listing in listings]

        else:
            listings = db.session.query(SDListing.neighbourhood, db.func.count(
                SDListing.id)).group_by(SDListing.neighbourhood).all()

            result = [{'neighbourhood': listing[0],
                       'listingsCount': listing[1]} for listing in listings]

        return jsonify(result)
