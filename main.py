from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="rootpassword",
    database="san_diego_airbnb_data"
)

mycursor = db.cursor()

app = Flask(__name__)
api = Api(app)


class Home(Resource):
    def get(self):
        result = "Welcome to my Python backend!"
        return result


class Neighbourhoods(Resource):
    def get(self):
        result = []

        mycursor.execute(
            "SELECT neighbourhood, COUNT(id) FROM sd_listings GROUP BY neighbourhood")

        for x in mycursor:
            obj = {
                "neighbourhood": x[0],
                "listingsCount": x[1]
            }
            result.append(obj)

        return result


api.add_resource(Home, "/")
api.add_resource(Neighbourhoods, "/neighbourhoods")


if __name__ == "__main__":
    app.run(debug=True)
