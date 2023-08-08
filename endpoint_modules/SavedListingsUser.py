from flask import jsonify, request, Response
from flask_restful import Resource
from common import db_connector
import datetime
import json

db, cursor = db_connector.DBConnector.connect()


class SavedListingsUser(Resource):
    def get(self, user_id):
        includeDetails = request.args.get("includeDetails")
        result = []

        if includeDetails == "true":
            columns = ["user_id", "listing_id", "name",
                       "host_id", "neighbourhood", "price"]

            cursor.execute("""
                SELECT saved_listings.user_id, saved_listings.listing_id, sd_listings.name, sd_listings.host_id, sd_listings.neighbourhood, sd_listings.price
                FROM saved_listings
                INNER JOIN sd_listings ON sd_listings.id = saved_listings.listing_id
                WHERE user_id = %s;
                """, (user_id,)
            )

        else:
            columns = ["id", "listing_id", "user_id", "date_saved"]

            cursor.execute(
                "SELECT * FROM saved_listings WHERE user_id = %s;", (user_id,))

        for x in cursor:
            result.append(dict(zip(columns, x)))

        json_result = json.dumps(
            result, cls=CustomJSONEncoder)

        return Response(json_result, content_type='application/json')

    def put(self, user_id):
        payload = request.get_json()
        listing_id = payload["listingId"]
        todaysDate = datetime.date.today()
        sql_date = todaysDate.strftime('%Y-%m-%d')

        cursor.execute(
            "SELECT * from saved_listings WHERE listing_id = %s AND user_id = %s;", (listing_id, user_id))

        for x in cursor:
            if x[0]:
                return "This listing has already been saved by this user"

        cursor.execute(
            f"INSERT INTO saved_listings(listing_id, user_id, date_saved) VALUES({listing_id},{user_id},'{sql_date}')")
        db.commit()

        return jsonify("listing successfully saved for user "+user_id)

    def delete(self, user_id):
        payload = request.get_json()
        listing_id = payload["listingId"]
        cursor.execute(
            f"DELETE FROM saved_listings WHERE listing_id = {listing_id} AND user_id = {user_id};")
        db.commit()

        return "listing deleted from saved list", 204


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        return super().default(obj)
