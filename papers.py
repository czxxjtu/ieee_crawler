# Author: Xu Wang
# Email: i@xuwang.im
#
# Filename: papers.py
#
#
from document import html_to_document,\
    journal_articles_requests_urls,\
    journal_article_total_number_from_url
from database import *
from nltk.corpus import stopwords
import re

class Publication:
    """
    Represent papers in a publication
    """
    def __init__(self, title):
        """

        :param title:
        :param last_rank: rank of last checked paper
        :return:
        """
        self.title = title
        self.issn = ''
        self.__id = None

    def get_last_rank(self, papers_table):
        """
        Retrieve the max rank
        :param papers_table: Publications table
        """
        return papers_table.get_max_rank_by_title(self.title)

    def get_total_number_of_articles(self):
        """

        """
        url = journal_articles_requests_urls(self.title)[0]
        return journal_article_total_number_from_url(url)


class Paper:
    """
    A paper
    """
    def __init__(self, publication, doc=None, remove_stopwords=False,
                 type=None):
        """

        :return:
        """
        self.publication = publication
        self.number = None  # Prime key
        self.doi = None
        self.spage = None
        self.epage = None
        self.issue = None
        self.partnum = None
        self.publicationid = None
        self.year = None
        self.rank = None
        self.title = None
        self.affiliation = None
        self.authors = None
        self.terms = None
        self.volume = None
        self.abstract = None
        self.type = type
        if doc is not None:
            self.from_dict(doc, remove_stopwords)

    def to_list(self):
        """
        fields:
        ----
        number
        doi
        spage
        epage
        issue
        partnum
        publication
        year
        rank
        title
        abstract
        authors
        terms
        ----
        :return:
        """
        type = self.type
        number = self.number
        if self.doi is not None:
            doi = self.doi
        else:
            doi = ''
        if self.spage is not None:
            spage = str(self.spage)
        else:
            spage = ''
        if self.epage is not None:
            epage = str(self.epage)
        else:
            epage = ''
        if self.issue is not None:
            issue = str(self.issue)
        else:
            issue = ''
        if self.partnum is not None:
            partnum = str(self.partnum)
        else:
            partnum = ''
        publication = self.publication
        if self.year is not None:
            year = str(self.year)
        else:
            year = ''
        rank = str(self.rank)
        if self.title is not None:
            title = self.title
        else:
            title = ''
        if self.abstract is not None:
            abstract = self.abstract
        else:
            abstract = ''
        if len(self.authors) > 0:
            authors = '|'.join(self.authors)
        else:
            authors = ''
        if len(self.terms) > 0:
            terms = '|'.join(self.terms)
        else:
            terms = ''
        if self.affiliation is not None:
            affiliation = self.affiliation
        else:
            affiliation = ''

        result = [type, number, doi, spage, epage, issue,
                  partnum, publication, year, rank, title,
                  abstract, authors, terms, affiliation]
        # fields = ['number', 'doi', 'spage', 'epage', 'issue', 'partnum',
        #           'publication', 'year', 'rank', 'title', 'abstract',
        #           'authors', 'terms', 'affiliation']

        return result

    def from_dict(self, doc, remove_stopwords=True):
        """

        :param doc: a dict generated by html_to_document
        :return:
        """
        self.rank = doc['rank']
        self.title = doc['title']
        if 'authors' in doc:
            self.authors = doc['authors']
        else:
            self.authors = []
        if 'affiliations' in doc:
            self.affiliation = doc['affiliations']
        if 'terms' in doc:
            self.terms = doc['terms']
        else:
            self.terms = []
        if 'volume' in doc:
            self.volume = doc['volume']
        if 'py' in doc:
            self.year = doc['py']
        if 'spage' in doc:
            self.spage = doc['spage']
        if 'epage' in doc:
            self.epage = doc['epage']
        if 'abstract' in doc:
            if remove_stopwords:
                self.abstract = self.__remove_stopwords(doc['abstract'])
            else:
                self.abstract = doc['abstract']
        self.number = doc['arnumber']
        if 'doi' in doc:
            self.doi = doc['doi']
        if 'issue' in doc:
            self.issue = doc['issue']
        if 'partnum' in doc:
            self.partnum = doc['partnum']
        if 'publicationid' in doc:
            self.publicationid = doc['publicationid']
        self.rank = doc['rank']
        self.title = doc['title']
        if 'terms' in doc:
            self.terms = doc['terms']

    def __from_html(self, bs4html):
        doc = html_to_document(bs4html)
        self.rank = doc['rank']
        self.title = doc['title']
        if 'authors' in doc:
            self.authors = doc['authors']
        if 'affiliations' in doc:
            self.affiliation = doc['affiliations']
        if 'terms' in doc:
            self.terms = doc['terms']
        if 'volume' in doc:
            self.volume = doc['volume']
        if 'py' in doc:
            self.year = doc['py']
        if 'spage' in doc:
            self.spage = doc['spage']
        if 'epage' in doc:
            self.epage = doc['epage']
        if 'abstract' in doc:
            self.abstract = doc['abstract']
            self.abstract = self.__remove_stopwords(self.abstract)
        self.number = doc['arnumber']
        if 'doi' in doc:
            self.doi = doc['doi']
        if 'issue' in doc:
            self.issue = doc['issue']
        if 'partnum' in doc:
            self.partnum = doc['partnum']
        if 'publicationid' in doc:
            self.publicationid = doc['publicationid']
        self.rank = doc['rank']
        self.title = doc['title']
        if 'terms' in doc:
            self.terms = doc['terms']

    def __str__(self):
        """

        :return:
        """
        pass

    def __remove_stopwords(self, s):
        """

        :param s:
        :return:
        """
        cached = stopwords.words('english')
        s1 = re.sub('[\W\b]', ' ', s.lower())
        return ' '.join([w for w in s1.split(' ') if w not in cached and len(w) > 0])
