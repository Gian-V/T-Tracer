# import mariadb
# import sys
#
# # Connect to MariaDB Platform
# try:
#     conn = mariadb.connect(
#         user="TTRW",
#         password="jArkqhHW2cJNSLD8",
#         host="64.225.96.112",
#         port=3306,
#         database="T_Tracer"
#
#     )
# except mariadb.Error as e:
#     print(f"Error connecting to MariaDB Platform: {e}")
#     sys.exit(1)
#
# # Get Cursor
# cur = conn.cursor(named_tuple=True)
#
# cur.execute("SELECT GPS_log FROM shipments")
#
# obj = cur.fetchone().GPS_log
# print(obj)


import bcrypt

password = "tonnolotti"
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(prefix=b"2a"))
print(hashed_password.decode('utf-8'))
