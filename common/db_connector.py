import mysql.connector


class DBConnector:
    @classmethod
    def connect(cls):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="rootpassword",
            database="san_diego_airbnb_data"
        )

        cursor = db.cursor()
        return db, cursor
