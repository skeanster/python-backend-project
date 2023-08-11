import mysql.connector
from flask import Flask, jsonify
from flask_restful import Api, Resource
from common.orm_db_config import db

# Endpoint Modules
from endpoint_modules import User, SavedListingsUser, Users, ListingsByPrice, SavedListings
from orm_endpoint_modules import Neighbourhoods

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:rootpassword@localhost/san_diego_airbnb_data'
db.init_app(app)
api = Api(app)


class Home(Resource):
    def get(self):
        result = "Welcome to my Python backend!"
        return jsonify(result)


api.add_resource(Home, "/", methods=['GET'])
api.add_resource(Neighbourhoods.Neighbourhoods,
                 "/neighbourhoods", methods=['GET'])
api.add_resource(ListingsByPrice.ListingsByPrice,
                 "/listingsByPrice", methods=['GET'])
api.add_resource(Users.Users, "/users", methods=['GET', 'POST'])
api.add_resource(User.User, "/users/<string:user_id>",
                 methods=['GET', 'DELETE'])
api.add_resource(SavedListings.SavedListings,
                 "/savedListings", methods=['GET'])
api.add_resource(SavedListingsUser.SavedListingsUser,
                 "/savedListings/<string:user_id>", methods=['GET', 'PUT', 'DELETE'])

if __name__ == "__main__":
    app.run(debug=True)
