# Author: Xu Wang
# Email: i@xuwang.im
#
# Filename: samair_ru.py
#
#

from sqlalchemy import *
import time
from multiprocessing import Process, Queue
from .Proxy import Proxy
# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)


def engine_connection():
    """
    Return a meta data of the connection
    :return:
    """
    from .config import db_database, db_user, db_passwd, db_host
    connection = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8'\
                 % (db_user, db_passwd, db_host, db_database)
    return create_engine(connection, pool_recycle=5)


def get_table(table, metadata):
    """
    Return the object of Table table in database bind to metadata
    :param metadata: metadata bind to a database connection
    :param table: table name
    :return: table object in sqlalchemy
    """
    return Table(table, metadata, autoload=True)

def get_free_proxy(Proxies, max_fails=5):
    """
    Get a free (non inuse) proxy
    :param Proxies: Proxy table
    :param max_fails: If a server has been failed for max_fails times (recent_fails), then do not validate it.
    :return: Proxy or None if all in use
    """
    s = Proxies.select(and_(Proxies.c.inuse == 0, Proxies.c.recent_fails <= max_fails),
                       order_by=asc(Proxies.c.last_update)).execute().fetchone()
    if s is not None:
        proxy = sql_result_to_proxy(s)
        return proxy
    else:
        return None


def lock_free_proxy(proxy, Proxies):
    """
    Lock proxy in Proxies (set inuse to 1)
    :param proxy: a Proxy server
    :param Proxies: Proxies table
    :return: None
    """
    set_proxy_inuse(proxy, 1, Proxies)


def get_and_lock_proxy(Proxies):
    """
    Get a free proxy and lock it
    :param Proxies: Proxies table
    :return: a Proxy server or None if all in use
    """
    proxy = get_free_proxy(Proxies)
    if proxy is not None:
        lock_free_proxy(proxy, Proxies)
        return proxy
    else:
        return None

def unlock_proxy(proxy, Proxies):
    """
    Set proxy inuse to 0
    :param proxy: a Proxy server
    :param Proxies: Proxies table
    :return: None
    """
    set_proxy_inuse(proxy, 0, Proxies)


def set_proxy_inuse(proxy, inuse, Proxies):
    """
    Set inuse of proxy in Proxies table
    :param proxy: a Proxy server
    :param inuse: 0 or 1
    :param Proxies: Proxies table
    :return:
    """
    if inuse not in [0, 1]:
        raise ValueError('Illegal value for inuse')

    Proxies.update(and_(Proxies.c.ip == proxy.ip,
                    Proxies.c.port == proxy.port,
                    Proxies.c.protocol == proxy.protocol)).execute(inuse=inuse)


def add_server(proxy, Proxies):
    """
    Add a server to the table
    :param ip:
    :param port:
    :param type:
    :param location:
    :return:
    """
    try:
        Proxies.insert().execute(ip=proxy.ip,
                                 port=proxy.port,
                                 anonymous=proxy.anonymous,
                                 location=proxy.location,
                                 protocol=proxy.protocol,
                                 passed=proxy.passed,
                                 tests=proxy.tests,
                                 recent_fails=proxy.recent_fails)
    except:
        pass


def process_verify_server(Proxies):
    """
    Verify every server in the table
    :return:
    """
    sleep_time = 300  # 5 minutes
    while True:
        s = get_and_lock_proxy(Proxies)
        if s is None:
            time.sleep(sleep_time)
        else:
            proxy = sql_result_to_proxy(s)
            working = proxy.validate()
            update_validate_result_proxy(proxy, Proxies, working)
            unlock_proxy(proxy, Proxies)

def update_validate_result_proxy(proxy, Proxies, working):
    """
    When proxy.validate is finished, update validate results
    :param proxy:
    :param Proxies:
    :param working:
    :return:
    """
    tests = proxy.tests + 1
    if working:
        passed = proxy.passed + 1
        recent_fails = 0
    else:
        passed = proxy.passed
        recent_fails = proxy.recent_fails + 1
    last_update = int(time.time())
    update = Proxies.update(and_(Proxies.c.ip == proxy.ip,
                                 Proxies.c.port == proxy.port,
                                 Proxies.c.protocol == proxy.protocol))
    try:
        update.execute(passed=passed,
                       tests=tests,
                       recent_fails=recent_fails,
                       last_update=last_update)
    except:
        pass


def sql_result_to_proxy(s):
    """
    Create a Proxy from result (a ResultProxy, or dict)
    :param s: a ResultProxy
    :return: Proxy
    """
    return Proxy(ip=s['ip'], port=s['port'], location=s['location'],
                 anonymous=s['anonymous'], protocol=s['protocol'], passed=s['passed'],
                 tests=s['tests'], recent_fails=s['recent_fails'])


def mp_process_verify_server_reader(queue, Proxies):
    """
    Take a server and add it to queue, so that verifiers can verify it
    :param queue:
    :return:
    """
    sleep_time = 300
    while True:
        s = get_and_lock_proxy(Proxies)
        if s is None:
            time.sleep(sleep_time)
        else:
            queue.put(s)

def mp_process_verify_server_writer(queue, Proxies):
    """
    Take a server from queue and add it to table
    :param queue:
    :return:
    """
    while True:
        proxy, working = queue.get()
        update_validate_result_proxy(proxy, Proxies, working)
        unlock_proxy(proxy, Proxies)

def mp_process_verify_server_verifier(inqueue, outqueue):
    """
    Take a server from inqueue, verify it and send it to outqueue
    :param inqueue:
    :param outqueue:
    :return:
    """
    while True:
        s = inqueue.get()
        proxy = s
        # proxy = sql_result_to_proxy(s)
        print('verifying', proxy)
        v = proxy.validate()
        outqueue.put((s, v))

def get_proxy_server(Proxies):
    """
    Get a proxy server that is available and not recently used.
    :param Proxies: Proxies table
    :return: a Proxy
    """
    return Proxies.select(and_(Proxies.c.inuse == 0,
                               Proxies.c.recent_fails == 0,
                               Proxies.c.location != 'China',
                               Proxies.c.anonymous.like('%anonymous%'),
                               Proxies.c.location != 'China'),
                          order_by=asc(Proxies.c.last_used)).execute().fetchone()


def set_proxy_server_last_used(proxy, Proxies, last_used=int(time.time())):
    """
    Set the last_used time of proxy in Proxies
    :param proxy: a Proxy server
    :param Proxies: Proxies table
    :return: None
    """
    update = Proxies.update(and_(Proxies.c.ip == proxy.ip,
                                 Proxies.c.port == proxy.port,
                                 Proxies.c.protocol == proxy.protocol))
    update.execute(last_used=last_used)


def get_proxy_server_set_last_used(Proxies):
    """
    ...
    :param Proxies:
    :return:
    """
    proxy = get_proxy_server(Proxies)
    set_proxy_server_last_used(proxy, Proxies)
    return sql_result_to_proxy(proxy)


def get_proxy_table():
    """
    Return Proxies table
    :return:
    """
    from .config import proxy_table
    engine = engine_connection()
    metadata = MetaData(bind=engine)
    return get_table(proxy_table, metadata)

