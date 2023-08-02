from flask import jsonify
from flask_restful import Resource
from common import db_connector
from collections import defaultdict

db, cursor = db_connector.DBConnector.connect()


class SavedListings(Resource):
    def get(self):
        result = []
        grouped_data = defaultdict(list)
        columns = ["id", "listing_id", "user_id"]

        cursor.execute(
            "SELECT id, listing_id, user_id FROM saved_listings")

        for x in cursor:
            item = (dict(zip(columns, x)))
            user_id = item['user_id']
            grouped_data[user_id].append(item)

        for user_id, items in grouped_data.items():
            user_object = {
                'user_id': user_id,
                'userSavedListings': items
            }
            result.append(user_object)

        return jsonify(result)
