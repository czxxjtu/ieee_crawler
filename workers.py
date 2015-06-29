

from database import *
from papers import *
from document import *
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)

def write_paper_to_db(paper, papers_table, terms_table,
                      paperterms_table, authors_table,
                      paperauthors_table):
    """

    :param paper:
    :param papers_table:
    :param terms_table:
    :param paperterms_table:
    :param authors_table:
    :param paperauthors_table:
    :return:
    """
    papers_table.add_paper(paper)
    print(paper.terms)
    for t in paper.terms:
        tid = terms_table.get_id_or_add(t)
        if not paperterms_table.exists_paper_term_by_id(paper.number, tid):
            paperterms_table.add_paper_term_by_id(paper.number, tid)

    for a in paper.authors:
        aid = authors_table.get_id_or_add(a)
        if not paperauthors_table.exists_paper_author_by_id(paper.number, aid):
            paperauthors_table.add_paper_author_by_id(paper.number, aid)


def retrieve_papers(publication, papers_table, terms_table,
                    paperterms_table, authors_table,
                    paperauthors_table):
    """

    :param publication:
    :return:
    """
    current = publication.get_last_rank(papers_table)
    urls = journal_articles_requests_urls(publication.title, cur=current,
                                          articles_per_request=1000)
    for url in urls:
        print('read --', url)
        paper_dicts = retrieve_documents_from_url(url)
        paperlist = []
        for pd in paper_dicts:
            paperlist.append(Paper(publication.title, pd))
        for p in paperlist:
            write_paper_to_db(p, papers_table, terms_table,
                              paperterms_table, authors_table,
                              paperauthors_table)


def get_publication(publications_table):
    """
    Return a publication name for retrieve_paper to use
    :param publications_table:
    :return:
    """
    return publications_table.get_empty_publication()


if __name__ == '__main__':
    publications_table = Publications()
    papers_table = Papers()
    terms_table = Terms()
    paperterms_table = PaperTerms()
    authors_table = Authors()
    paperauthors_table = PaperAuthors()
    # ptitle = 'Aerospace, IEEE Transactions on'
    for ptitle in publications_table.get_all_publications_title():
        publication = Publication(ptitle)
        retrieve_papers(publication, papers_table, terms_table,
                        paperterms_table, authors_table,
                        paperauthors_table)
