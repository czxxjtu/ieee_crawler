from database import Publications
from papers import *
from document import *
import csv
from document import journal_articles_requests_urls,\
    retrieve_documents_from_url
import os.path


def retrieve_papers_to_tsv(ptitle):
    """

    :param publication:
    :param filename:
    :return:
    """
    ptitle_f = ptitle.replace('/', ' ')
    filename = 'tsv/' + ptitle_f + '.tsv'
    if os.path.isfile(filename):
        return
    fields = ['number', 'doi', 'spage', 'epage', 'issue', 'partnum',
              'publication', 'year', 'rank', 'title', 'abstract',
              'authors', 'terms']
    with open(filename, 'ta', newline='') as fp:
        tsv_writer = csv.writer(fp, delimiter='\t')
        tsv_writer.writerow(fields)
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
                        p = Paper(ptitle, pd)
                        paperlist.append(p)
                    paper_str_list = []
                    for p in paperlist:
                        paper_str_list.append(p.to_list())
                    tsv_writer.writerows(paper_str_list)
                except Exception as e:
                    print(str(e))
        except Exception as e:
            print(str(e))


if __name__ == '__main__':

    publications_table = Publications()
    for ptitle in publications_table.get_all_publications_title():
        retrieve_papers_to_tsv(ptitle)