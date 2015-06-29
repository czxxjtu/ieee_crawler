# Author: Xu Wang
# Email: i@xuwang.im
#
# Filename: document.py
#
#
from bs4 import BeautifulSoup as bs
import requests


def journal_article_total_number(bs4html):
    return int(bs4html.find('root').find('totalfound').text)


def journal_article_total_number_from_url(url):
    r = requests.get(url)
    soup = bs(r.text)
    return journal_article_total_number(soup)


def journal_articles_requests_urls(title, cur=1, articles_per_request=200):
    base_url = 'http://ieeexplore.ieee.org/gateway/ipsSearch.jsp?jn=%s&hc=%d&rs=%d&sortfield=py&sortorder=asc'
    url = base_url % (title, 0, 1)
    total_articles = journal_article_total_number_from_url(url)
    urls = []
    while cur <= total_articles:
        url = base_url % (title, articles_per_request, cur)
        urls.append(url)
        cur += articles_per_request
    return urls


def document_rank(bs4html):
    return int(bs4html.find('rank').text)


def document_title(bs4html):
    return bs4html.find('title').text


def document_authors(bs4html):
    authors = []
    for a in bs4html.find('authors').text.split(';'):
        if len(a) == 0:
            return authors
        else:
            au = a.strip()
            if len(au) > 0:
               authors.append(a.strip())
    return authors


def document_affiliations(bs4html):
    return bs4html.find('affiliations').text


def document_terms(bs4html):
    thesaurusterms = bs4html.find('thesaurusterms')
    terms = []
    for t in thesaurusterms.findAll('term'):

        terms.append(t.text)
    return terms


def document_publication_title(bs4html):
    return bs4html.find('pubtitle').text


def document_publication_number(bs4html):
    return int(bs4html.find('punumber').text)


def document_publication_type(bs4html):
    return bs4html.find('pubtype').text


def document_publisher(bs4html):
    return bs4html.find('publisher').text


def document_volume(bs4html):
    return int(bs4html.find('volume').text)


def document_issue(bs4html):
    return int(bs4html.find('issue').text)


def document_publish_year(bs4html):
    return int(bs4html.find('py').text)


def document_page_range(bs4html):
    spage = int(bs4html.find('spage').text)
    epage = int(bs4html.find('epage').text)
    return spage, epage


def document_abstract(bs4html):
    abstract = bs4html.find('abstract').text
    none_abstract_str = 'First Page of the Article'
    if none_abstract_str in abstract:
        return None
    else:
        return abstract


def document_publication_issn(bs4html):
    return bs4html.find('issn').text


def document_article_number(bs4html):
    return bs4html.find('arnumber').text


def document_doi(bs4html):
    return bs4html.find('doi').text


def document_publication_id(bs4html):
    return int(bs4html.find('publicationid').text)


def document_partnum(bs4html):
    return int(bs4html.find('partnum').text)


def document_url(bs4html):
    return bs4html.find('mdurl').text


def document_pdf_url(bs4html):
    return bs4html.find('pdf').text


def html_to_document(bs4html):
    doc = {'rank': document_rank(bs4html), 'title': document_title(bs4html)}
    authors = document_authors(bs4html)
    # if len(authors) > 0:
    #     doc['authors'] = authors
    doc['authors'] = authors

    try:
        doc['affiliations'] = document_affiliations(bs4html)
    except:
        pass

    try:
        terms = document_terms(bs4html)
        if len(terms) > 0:
            doc['terms'] = terms
    except:
        pass

    try:
        doc['pubtitle'] = document_publication_title(bs4html)
    except:
        pass

    try:
        doc['punumber'] = document_publication_number(bs4html)
    except:
        pass

    try:
        doc['pubtype'] = document_publication_type(bs4html)
    except:
        pass

    try:
        doc['publisher'] = document_publisher(bs4html)
    except:
        pass

    try:
        doc['volume'] = document_volume(bs4html)
    except:
        pass

    try:
        doc['issue'] = document_issue(bs4html)
    except:
        pass

    try:
        doc['py'] = document_publish_year(bs4html)
    except:
        pass

    try:
        spage, epage = document_page_range(bs4html)
        doc['spage'] = spage
        doc['epage'] = epage
    except:
        pass

    try:
        abstract = document_abstract(bs4html)
        if abstract is not None:
            doc['abstract'] = abstract
    except:
        pass

    try:
        doc['issn'] = document_publication_issn(bs4html)
    except:
        pass

    doc['arnumber'] = document_article_number(bs4html)

    try:
        doc['doi'] = document_doi(bs4html)
    except:
        pass

    try:
        doc['publicationid'] = document_publication_id(bs4html)
    except:
        pass

    try:
        doc['partnum'] = document_partnum(bs4html)
    except:
        pass

    try:
        doc['url'] = document_url(bs4html)
    except:
        pass

    try:
        doc['pdfurl'] = document_pdf_url(bs4html)
    except:
        pass

    return doc


def retrieve_documents_from_url(url):
    jr = requests.get(url)
    jsoup = bs(jr.text)
    documents = jsoup.findAll('document')
    docs = []
    for d in documents:
        docs.append(html_to_document(d))
    return docs


