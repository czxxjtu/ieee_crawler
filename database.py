# Author: Xu Wang
# Email: i@xuwang.im
#
# Filename: database.py
#
#
from sqlalchemy import *
import sqlalchemy
import config
from utils import log
import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)

con = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8'\
      % (config.db_user, config.db_passwd, config.db_host, config.db_database)
engine = create_engine(con, pool_recycle=5)

def engine_connection():
    """
    Return a meta data of the connection
    :return:
    """
    # connection = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8'\
    #              % (config.db_user, config.db_passwd, config.db_host, config.db_database)
    # return MetaData(bind=create_engine(connection, pool_recycle=5))
    return MetaData(bind=engine)


def get_table(table_name, metadata):
    """
    Return the object of Table table in database bind to metadata
    :param metadata: metadata bind to a database connection
    :param table_name: table name
    :return: table object in sqlalchemy
    """
    return Table(table_name, metadata, autoload=True)


class Publications:
    """
    Publications table
    """
    def __init__(self, _table=None):
        """
        Create a connection to the table
        :param _table:
        :return:
        """
        if _table is not None:
            self.__table = get_table(_table, engine_connection())
        else:
            self.__table = get_table(config.PublicationsTableName, engine_connection())

    def exist_by_name(self, name):
        """
        If name exists in table or not
        :param name: Publication name
        :return:
        """
        pub = self.__table.select(self.__table.c.name == name).execute().fetchone()
        if pub is not None:
            return True
        else:
            return False

    def exist_by_number(self, number):
        """
        If a number (by ieee) exists or not
        :param number:
        :return:
        """
        pub = self.__table.select(self.__table.c.number == number).execute().fetchone()
        if pub is not None:
            return True
        else:
            return False

    def add_publication_title_type_number(self, title, type, number):
        """
        Add a publication and fills only name, type and number
        :param title:
        :param type:
        :param number:
        :return:
        """
        try:
            self.__table.insert().execute(title=title,
                                          type=type,
                                          number=number)
        except Exception as e:
            print(str(e))

    def get_empty_publication(self):
        """
        get an un-updated publication
        :return:
        """
        row = self.__table.select(self.__table.c.last_update == 0).execute().fetchone()
        return row

    def get_all_publications_title(self):
        """

        """
        rows = self.__table.select().execute().fetchall()
        titles = []
        for r in rows:
            titles.append(r['title'])
        return titles


class Papers:
    """
    Paper table
    """
    def __init__(self, _table=None):
        """
        Create a connection to the table
        :param _table:
        :return:
        """
        if _table is not None:
            self.__table = get_table(_table, engine_connection())
        else:
            self.__table = get_table(config.PapersTableName, engine_connection())

    def exist_by_number(self, number):
        """
        A paper with 'number' exists or not
        :param number:
        :return:
        """
        p = self.__table.select(self.__table.c.number == number).execute().fetchone()
        if p is None:
            return False
        else:
            return True

    def add_paper(self, paper):
        """
        Add paper to table
        :param paper: a Paper object
        :return:
        """
        try:
            self.__table.insert().execute(number=paper.number,
                                          doi=paper.doi,
                                          spage=paper.spage,
                                          epage=paper.epage,
                                          issue=paper.issue,
                                          partnum=paper.partnum,
                                          publication=paper.publication,
                                          year=paper.year,
                                          rank=paper.rank,
                                          title=paper.title,
                                          abstract=paper.abstract)
        except Exception as e:
            log(str(e))

    def get_max_rank_by_title(self, ptitle):
        """

        """
        s = self.__table.select(self.__table.c.publication == ptitle,
                                order_by=desc(self.__table.c.rank))
        row = s.execute().fetchone()
        if row is None:
            r = 1
        else:
            r = row['rank']
        return r


class Terms:
    """
    Terms table
    """
    def __init__(self, _table=None):
        """

        :param _table:
        :return:
        """
        if _table is not None:
            self.__table = get_table(_table, engine_connection())
        else:
            self.__table = get_table(config.TermsTableName, engine_connection())

    def exists_term(self, term):
        """

        :param term:
        :return:
        """
        t = self.__table.select(self.__table.c.term == term).execute().fetchone()
        if t is None:
            return False
        else:
            return True

    def add_term(self, term):
        """

        :param term:
        :return:
        """
        try:
            self.__table.insert().execute(term=term)
        except Exception as e:
            log(str(e))

    def add_terms(self, term_list):
        """

        :param term_list:
        :return:
        """
        for term in term_list:
            self.add_term(term)

    def get_id(self, term):
        """
        Get term id for term
        :param term:
        :return:
        """
        row = self.__table.select(self.__table.c.term == term).execute().fetchone()
        return row['id']

    def get_id_or_add(self, term):
        """

        """
        if not self.exists_term(term):
            self.add_term(term)
        return self.get_id(term)


class PaperTerms:
    """
    PaperTerms table
    """
    def __init__(self, _table=None):
        """

        :param _table:
        :return:
        """
        if _table is not None:
            self.__table = get_table(_table, engine_connection())
        else:
            self.__table = get_table(config.PaperTermsTableName, engine_connection())

    def exists_paper_term_by_id(self, paper_id, term_id):
        """

        :param paper_id:
        :param term_id:
        :return:
        """
        pt = self.__table.select(and_(self.__table.c.paperid == paper_id,
                                      self.__table.c.termid == term_id)).execute().fetchone()
        if pt is None:
            return False
        else:
            return True

    def add_paper_term_by_id(self, paper_id, term_id):
        """

        :param paper_id:
        :param term_id:
        :return:
        """
        try:
            self.__table.insert().execute(paperid=paper_id,
                                          termid=term_id)
        except Exception as e:
            log(str(e))

    def add_paper_term_by_term(self, paper_id, term_name, term_table):
        """

        :param paper_id:
        :param term_name:
        :param term_table:
        :return:
        """
        term_id = term_table.get_id(term_name)
        self.add_paper_term_by_id(paper_id, term_id)


class Authors:
    """
    Authors table
    """
    def __init__(self, _table=None):
        """

        :param _table:
        :return:
        """
        if _table is not None:
            self.__table = get_table(_table, engine_connection())
        else:
            self.__table = get_table(config.AuthorsTableName, engine_connection())

    def exists_author(self, author_name):
        """

        :param author_name:
        :return:
        """
        a = self.__table.select(self.__table.c.name == author_name).execute().fetchone()
        if a is None:
            return False
        else:
            return True

    def add_author(self, author_name):
        """

        :param author_name:
        :return:
        """
        try:
            self.__table.insert().execute(name=author_name)
        except Exception as e:
            log(str(e))

    def add_authors(self, author_list):
        """

        :param author_list:
        :return:
        """
        for author_name in author_list:
            self.add_author(author_name)

    def get_id(self, author_name):
        """

        :param author_name:
        :return:
        """
        row = self.__table.select(self.__table.c.name == author_name).execute().fetchone()
        return row['id']

    def get_id_or_add(self, author_name):
        """

        """
        if not self.exists_author(author_name):
            self.add_author(author_name)
        return self.get_id(author_name)


class PaperAuthors:
    """
    PaperAuthors table
    """
    def __init__(self, _table=None):
        """

        :param _table:
        :return:
        """
        if _table is not None:
            self.__table = get_table(_table, engine_connection())
        else:
            self.__table = get_table(config.PaperAuthorsTableName, engine_connection())

    def exists_paper_author_by_id(self, paper_id, author_id):
        """

        :param paper_id:
        :param author_id:
        :return:
        """
        pa = self.__table.select(and_(self.__table.c.paperid == paper_id,
                                      self.__table.c.authorid == author_id)).execute()\
                                                                            .fetchone()
        if pa is None:
            return False
        else:
            return True

    def add_paper_author_by_id(self, paper_id, author_id):
        """

        :param paper_id:
        :param author_id:
        :return:
        """
        try:
            self.__table.insert().execute(paperid=paper_id,
                                          authorid=author_id)
        except Exception as e:
            log(str(e))

    def add_paper_author_by_author(self, paper_id, author_name, author_table):
        """

        :param paper_id:
        :param author_name:
        :param author_table:
        :return:
        """
        author_id = author_table.get_id(author_name)
        self.add_paper_author_by_id(paper_id, author_id)


class Publisher:
    """
    Publisher table
    """
    def __init__(self, _table=None):
        """

        :param _table:
        :return:
        """
        if _table is not None:
            self.__table = get_table(_table, engine_connection())
        else:
            self.__table = get_table(config.PublishersTableName, engine_connection())

    def exists_publisher(self, publisher_name):
        """

        :param publisher_name:
        :return:
        """
        p = self.__table.select(self.__table.c.name == publisher_name).execute().fetchone()
        if p is None:
            return False
        else:
            return True

    def add_publisher(self, publisher_name):
        """

        :param publisher_name:
        :return:
        """
        self.__table.insert().execute(name=publisher_name)

    def get_id(self, publisher_name):
        """

        :param publisher_name:
        :return:
        """
        row = self.__table.select(self.__table.c.name == publisher_name).execute().fetchone()
        return row['id']

    def get_id_or_add(self, publisher_name):
        """

        :param publisher_name:
        :return:
        """
        if not self.exists_publisher(publisher_name):
            self.add_publisher(publisher_name)
        return self.get_id(publisher_name)