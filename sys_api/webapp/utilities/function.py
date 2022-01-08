import mariadb

from webapp.utilities.variables import db


async def get_db():
    cur = db.cursor()
    try:
        yield cur
    finally:
        cur.close()


def load_gps(cursor: mariadb.connection.cursor, gps_str: str):
    shipment_id, latitude, longitude, datetime = gps_str.split("|")
    cursor.execute("SELECT GPS_log from shipments where id = {};".format(int(shipment_id)))
    gps_log = cursor.fetchone()
    gps_log = "" if gps_log is None else gps_log
    gps_log += "{date: " + datetime + ", latitude: " + latitude + ", longitude: " + longitude + "}"
    cursor.execute("UPDATE shipments SET GPS_log = '{}' WHERE id = {};".format(gps_log, int(shipment_id)))
