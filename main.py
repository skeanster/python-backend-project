from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="rootpassword",
    database="san_diego_airbnb_data"
)

cursor = db.cursor()

app = Flask(__name__)
api = Api(app)


class Home(Resource):
    def get(self):
        result = "Welcome to my Python backend!"
        return result


class Neighbourhoods(Resource):
    def get(self):
        result = []
        location = request.args.get("location")

        if location:
            cursor.execute(
                "SELECT * FROM sd_listings WHERE neighbourhood = '" + location + "';")

            columns = [col[0] for col in cursor.description]
            for x in cursor:
                result.append(dict(zip(columns, x)))

            return jsonify(result)

        cursor.execute(
            "SELECT neighbourhood, COUNT(id) FROM sd_listings GROUP BY neighbourhood")

        for x in cursor:
            obj = {
                "neighbourhood": x[0],
                "listingsCount": x[1]
            }
            result.append(obj)

        return jsonify(result)


class ListingsByPrice(Resource):
    def get(self):
        result = []
        sql = "SELECT * FROM sd_listings WHERE 1"
        minprice = request.args.get("minprice")
        maxprice = request.args.get("maxprice")
        location = request.args.get("location")

        if maxprice:
            sql = sql + " AND price < "+maxprice+""

        if minprice:
            sql = sql + " AND price > "+minprice+""

        if location:
            sql = sql + " AND neighbourhood = '"+location+"'"

        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]

        for x in cursor:
            result.append(dict(zip(columns, x)))

        return jsonify(result)


api.add_resource(Home, "/")
api.add_resource(Neighbourhoods, "/neighbourhoods")
api.add_resource(ListingsByPrice, "/listingsByPrice")


if __name__ == "__main__":
    app.run(debug=True)
