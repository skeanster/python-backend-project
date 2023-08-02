from flask_restful import Resource
from common import db_connector
from flask import jsonify

db, cursor = db_connector.DBConnector.connect()


class User(Resource):
    def get(self, user_id):
        result = []
        columns = ["id", "name", "primaryNeighbourhood"]

        cursor.execute(
            "SELECT * FROM users WHERE id = "+user_id+";")

        for x in cursor:
            result.append(dict(zip(columns, x)))

        return jsonify(result)

    def delete(self, user_id):
        cursor.execute(
            "DELETE FROM users WHERE id = "+user_id+";")
        db.commit()

        return "user deleted", 204
