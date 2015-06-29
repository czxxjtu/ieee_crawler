# Author: Xu Wang
# Email: i@xuwang.im
#
# Filename: proxy_requests.py
#
#
from .proxy_manager.proxy_manager import get_proxy_server_set_last_used, get_proxy_table
from multiprocessing import Process, Queue
import requests
from utils import log
from time import sleep

def mp_proxy_server_reader(usable_proxy_queue):
    """
    take a proxy from Proxies and insert it into usable_proxy_queue (proxy, 1), where
    1 means the proxy will be used for the 1st time.
    :param usable_proxy_queue: Queue for usable proxy servers
    :return: None
    """
    Proxies = get_proxy_table()
    while True:
        proxy = get_proxy_server_set_last_used(Proxies)
        usable_proxy_queue.put((proxy, 1))


def mp_proxy_server_recycler(usable_proxy_queue, recycle_proxy_queue, max_use=2):
    """
    Get a proxy server from recycle_proxy_queue (proxy, x). If x <= max_use, put it to usable_proxy_queue again
    :param usable_proxy_queue:
    :param recycle_proxy_queue:
    :param max_use:
    :return:
    """
    while True:
        proxy, x = recycle_proxy_queue.get()
        if x <= max_use:
            usable_proxy_queue.put((proxy, x + 1))


def mp_open_url(url_queue, result_queue, usable_proxy_queue, recycle_proxy_queue,
                max_try=10, timeout=20, sleep_time=10):
    """
    Get a url from url_queue and a proxy from usable_proxy_queue, then open the url. Finally,
    return result to result_queue, and put the proxy to recycle_proxy_queue.
    :param url_queue: A pair (url, misc). open url and get its content
    :param result_queue: put content of url (string format) and misc as (content, misc)
    :param usable_proxy_queue:
    :param recycle_proxy_queue:
    :param sleep_time: sleep for a while after retrieves an url
    :return:
    """
    while True:
        url, misc = url_queue.get()
        tried = 0
        success_flag = False
        while (not success_flag) and (tried < max_try):

            sleep(sleep_time)

            proxy, proxy_use = usable_proxy_queue.get()
            proxies = {
                'http': str(proxy),
                'https': str(proxy)
            }
            try:
                log('get url start', url)
                r = requests.get(url, proxies=proxies, timeout=timeout)
                log('get url success and put in result_queue', url)
                result_queue.put((r.text, misc))
                success_flag = True
                log('put in result_queue fin', url)
            except:
                tried += 1
                log('get url retry', str(tried), url)

            recycle_proxy_queue.put((proxy, proxy_use))
        if tried == max_try:
            log('get url failed', url)
            url_queue.put((url, misc))


def proxy_requests(url_queue, result_queue, workers=1):
    """
    Given a url_queue, retrieve pages in url_queue and return it to result_queue
    :param url_queue:
    :param result_queue:
    :param workers:
    :return:
    """
    usable_proxy_queue = Queue(workers)
    recycle_proxy_queue = Queue()

    proxy_reader = Process(target=mp_proxy_server_reader,
                           args=(usable_proxy_queue, ))
    proxy_reader.start()
    proxy_recycler = Process(target=mp_proxy_server_recycler,
                             args=(usable_proxy_queue, recycle_proxy_queue))
    proxy_recycler.start()

    processes = []
    for i in range(workers):
        openner = Process(target=mp_open_url,
                          args=(url_queue, result_queue,
                                usable_proxy_queue,
                                recycle_proxy_queue))
        openner.start()
        processes.append(openner)



if __name__ == '__main__':
    url_queue = Queue()
    result_queue = Queue()
    usable_proxy_queue = Queue(1)
    recycle_proxy_queue = Queue(3)

    url = 'http://xuwang.im'
    url_queue.put((url, None))

    proxy_reader = Process(target=mp_proxy_server_reader, args=(usable_proxy_queue, ))
    proxy_reader.start()

    proxy_recycler = Process(target=mp_proxy_server_recycler, args=(usable_proxy_queue, recycle_proxy_queue))
    proxy_recycler.start()

    openner = Process(target=mp_open_url, args=(url_queue, result_queue, usable_proxy_queue, recycle_proxy_queue))
    openner.start()

    r, t = result_queue.get()
    print(r)

    proxy_recycler.join()
    proxy_reader.join()
    openner.join()
