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
        return jsonify(result)


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
        result = {"count": 0, "listings": []}
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
            result["listings"].append(dict(zip(columns, x)))
            result["count"] = result["count"] + 1

        return jsonify(result)


class Users(Resource):
    def get(self):
        result = {
            "totalUsers": 0,
            "users": []
        }
        columns = ["id", "name", "primaryNeighbourhood"]

        cursor.execute("SELECT * FROM users")

        for x in cursor:
            result["users"].append((dict(zip(columns, x))))
            result["totalUsers"] = result["totalUsers"] + 1

        return jsonify(result)

    def put(self):
        neighbourhood = ''
        request_neighbourhood = request.args.get("primaryNeighbourhood")
        if request_neighbourhood:
            neighbourhood = request_neighbourhood

        cursor.execute(
            "INSERT INTO users(name, primaryNeighbourhood)VALUES('"+request.args.get("name")+"','"+neighbourhood+"')")
        db.commit()

        return "User Added", 201


class User(Resource):
    def get(self, user_id):
        result = []
        columns = ["id", "name", "primaryNeighbourhood"]

        cursor.execute("SELECT * FROM users WHERE id = "+user_id+";")

        for x in cursor:
            result.append(dict(zip(columns, x)))

        return jsonify(result)

    def delete(self, user_id):
        cursor.execute("DELETE FROM users WHERE id = "+user_id+";")
        db.commit()

        return "user deleted", 204


api.add_resource(Home, "/")
api.add_resource(Neighbourhoods, "/neighbourhoods")
api.add_resource(ListingsByPrice, "/listingsByPrice")
api.add_resource(Users, "/users")
api.add_resource(User, "/users/<string:user_id>")

if __name__ == "__main__":
    app.run(debug=True)
