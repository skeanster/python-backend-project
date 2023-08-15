from flask import jsonify, request
from flask_restful import Resource
from common import db_connector

db, cursor = db_connector.DBConnector.connect()


class ListingsByPrice(Resource):
    def get(self):
        result = {"count": 0, "listings": []}
        sql = "SELECT * FROM sd_listings WHERE 1"
        minprice = request.args.get("minprice")
        maxprice = request.args.get("maxprice")
        location = request.args.get("location")
        params = []

        if maxprice:
            sql += " AND price < %s"
            params.append(maxprice)

        if minprice:
            sql += " AND price > %s"
            params.append(minprice)

        if location:
            sql += " AND neighbourhood = %s"
            params.append(location)

        cursor.execute(sql, params)

        columns = [col[0] for col in cursor.description]

        for x in cursor:
            result["listings"].append(dict(zip(columns, x)))
            result["count"] = result["count"] + 1

        return jsonify(result)
