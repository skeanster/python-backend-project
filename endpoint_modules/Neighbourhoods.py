from flask_restful import Resource
from common import db_connector
from flask import jsonify, request

db, cursor = db_connector.DBConnector.connect()


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
