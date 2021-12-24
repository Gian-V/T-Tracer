import sys
import mariadb
from typing import NamedTuple
from collections import namedtuple


try:
    db = mariadb.connect(
        user='TTRW',
        password='jArkqhHW2cJNSLD8',
        host='64.225.96.112',
        port=3306,
        database='T_Tracer'
    )
    db.autocommit = True
except mariadb.Error as e:
    sys.exit(1)


cur = db.cursor(named_tuple=True)
cur.execute('SELECT * FROM trucker;')
results = cur.fetchone()

print(dir(results))

x = [
    i for i in dir(results)
    if not callable(getattr(results, i)) and not i.startswith(
        ('__', 'n_fields', 'n_sequence_fields', 'n_unnamed_fields'))
]
