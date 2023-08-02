from flask import Flask, jsonify
from flask_restful import Api, Resource

# Endpoint Modules
from endpoint_modules import User, Neighbourhoods, SavedListingsUser, Users, ListingsByPrice, SavedListings

app = Flask(__name__)
api = Api(app)


class Home(Resource):
    def get(self):
        result = "Welcome to my Python backend!"
        return jsonify(result)


api.add_resource(Home, "/")
api.add_resource(Neighbourhoods.Neighbourhoods, "/neighbourhoods")
api.add_resource(ListingsByPrice.ListingsByPrice, "/listingsByPrice")
api.add_resource(Users.Users, "/users")
api.add_resource(User.User, "/users/<string:user_id>")
api.add_resource(SavedListings.SavedListings, "/savedListings")
api.add_resource(SavedListingsUser.SavedListingsUser,
                 "/savedListings/<string:user_id>")

if __name__ == "__main__":
    app.run(debug=True)
