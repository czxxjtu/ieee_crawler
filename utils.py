# Author: Xu Wang
# Email: i@xuwang.im
#
# Filename: utils.py
#
#
# Author: Xu Wang
# Email: i@xuwang.im
#
# Filename: utils.py
#
#
from sqlalchemy import *
import time
import datetime

def engine_connection():
    """
    Return a meta data of the connection
    :return:
    """
    from config import db_database, db_user, db_passwd, db_host
    connection = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8'\
                 % (db_user, db_passwd, db_host, db_database)
    return MetaData(connection)


# a connection
metadata = engine_connection()


def get_table(table_name, metadata=metadata):
    """
    Return the object of Table table in database bind to metadata
    :param metadata: metadata bind to a database connection
    :param table_name: table name
    :return: table object in sqlalchemy
    """
    return Table(table_name, metadata, autoload=True)


Logdb = get_table('Log')


def today():
    """
    Return today's date and time in string
    :return: date, time, timestamp
    """
    cur_date = datetime.datetime.now().strftime('%Y-%m-%d')
    cur_time = datetime.datetime.now().strftime('%H:%M:%S')
    timestamp = int(time.time())
    return cur_date, cur_time, timestamp


def log(*args):
    """
    Insert log to database
    :param result: a string of what has done
    :return:
    """
    import inspect
    caller = inspect.stack()[1][3]
    cur_date, cur_time, timestamp = today()
    Logdb.insert().execute(date=cur_date,
                           time=cur_time,
                           timestamp=timestamp,
                           operation=caller,
                           result=' '.join(args))
    print(' '.join([cur_date, cur_time, caller] + list(args)))


