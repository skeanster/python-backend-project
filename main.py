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


api.add_resource(Home, "/")

if __name__ == "__main__":
    app.run(debug=True)
