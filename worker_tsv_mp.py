from database import Publications
from papers import *
from document import *
import csv
from document import journal_articles_requests_urls,\
    retrieve_documents_from_url
import os.path
from multiprocessing import Process, Queue
import multiprocessing


def retrieve_papers_to_tsv(ptitle, ptype):
    """

    :param publication:
    :param filename:
    :return:
    """
    ptitle_f = ptitle.replace('/', ' ')
    filename = 'tsv/' + ptitle_f + '.tsv'
    if os.path.isfile(filename):
        return
    fields = ['type', 'number', 'doi', 'spage', 'epage', 'issue', 'partnum',
              'publication', 'year', 'rank', 'title', 'abstract',
              'authors', 'terms', 'affiliation']
    with open(filename, 'ta', newline='') as fp:
        tsv_writer = csv.writer(fp, delimiter='\t')
        # tsv_writer.writerow(fields)
        try:
            print('get publication urls', ptitle)
            urls = journal_articles_requests_urls(ptitle,
                                                  articles_per_request=1000)
            for url in urls:
                try:
                    print('reading --', url)
                    paper_dicts = retrieve_documents_from_url(url)
                    paperlist = []
                    for pd in paper_dicts:
                        p = Paper(ptitle, pd, type=ptype)
                        paperlist.append(p)
                    paper_str_list = []
                    for p in paperlist:
                        paper_str_list.append(p.to_list())
                    tsv_writer.writerows(paper_str_list)
                except Exception as e:
                    print(str(e))
        except Exception as e:
            print(str(e))


def mp_retriever(inqueue):
    """

    :param inqueue:
    :return:
    """
    while True:
        ptitle, ptype = inqueue.get()
        if ptitle is None:
            return
        else:
            retrieve_papers_to_tsv(ptitle, ptype)

if __name__ == '__main__':

    publications_table = Publications()
    workers = 128
    processes = []
    title_queue = Queue()
    for ptitle, ptype in publications_table.get_all_titles_numbers():
        # print(ptype, ptitle)
        # retrieve_papers_to_tsv(ptitle)
        title_queue.put((ptitle, ptype))

    for i in range(workers):
        title_queue.put((None, None))

    for i in range(workers):
        p = Process(target=mp_retriever, args=(title_queue, ))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

