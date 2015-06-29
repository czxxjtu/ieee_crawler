# Author: Xu Wang
# Email: i@xuwang.im
#
# Filename: journal.py
#
#
import requests
from bs4 import BeautifulSoup as bs


def journal_list_url():
    base = 'http://ieeexplore.ieee.org/xpl/periodicals.jsp?pageNumber=%d'
    return [base % i for i in range(1, 13)]


def journal_url_to_number(url):
    digits = '01234567899'
    num = ''
    for i in url[::-1]:
        if i in digits:
            num = i + num
        else:
            return num


def html_to_journal_title(bs4html):
    return bs4html.find(attrs={'class': 'journals-content-title'}).text.strip()


def html_to_journal_number(bs4html):
    return journal_url_to_number(bs4html.find('a')['href'])


def html_to_journal_history(bs4html):

    def li_to_journal_title(bs4htmlli):
        return bs4htmlli.find('a').text.strip()

    def li_to_journal_number(bs4htmlli):
        return html_to_journal_number(bs4htmlli)

    recent = bs4html.findAll(attrs={'class': 'RevealContent'})
    if len(recent) == 0:
        return []
    history = []
    for r in recent[0].findAll('li'):
        n = li_to_journal_number(r)
        t = li_to_journal_title(r)
        history.append((n, t))
    return history


def html_to_journal_all_titles(bs4html):
    result = []
    n = html_to_journal_number(bs4html)
    t = html_to_journal_title(bs4html)
    result.append((n, t))
    result += html_to_journal_history(bs4html)
    return result


def html_page_to_journals_list(html_text):
    bs4html = bs(html_text)
    journals = bs4html.findAll(attrs={'class': 'noTitleHistory'})
    result = []
    for j in journals:
        result += html_to_journal_all_titles(j)
    return result


def all_journal_titles():
    result = []
    for url in journal_list_url():
        print(url)
        r = requests.get(url)
        result += html_page_to_journals_list(r.text)
    return result
