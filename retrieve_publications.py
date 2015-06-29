# Author: Xu Wang
# Email: i@xuwang.im
#
# Filename: retrieve_publications.py
#
#
from database import Publications
from journal import *

PublicationsTable = Publications()

# retrieve journals
publication_type = 'Journals & Magazines'
for number, name in all_journal_titles():
    print(name, number)
    PublicationsTable.add_publication_title_type_number(name, publication_type, number)
