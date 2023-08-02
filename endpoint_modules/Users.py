from flask import jsonify, request
from flask_restful import Resource
from common import db_connector

db, cursor = db_connector.DBConnector.connect()


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

    def post(self):
        neighbourhood = ''
        request_neighbourhood = request.args.get("primaryNeighbourhood")
        if request_neighbourhood:
            neighbourhood = request_neighbourhood

        cursor.execute(
            "INSERT INTO users(name, primaryNeighbourhood)VALUES('"+request.args.get("name")+"','"+neighbourhood+"')")
        db.commit()

        return "User Added", 201
