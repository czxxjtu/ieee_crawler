import csv


def extract_one_paper(paper_row):
    """

    :param paper_row: one paper
    :return:
    """
    # input fields
    # fields = ['type', 'number', 'doi', 'spage', 'epage', 'issue', 'partnum',
    #           'publication', 'year', 'rank', 'title', 'abstract',
    #           'authors', 'terms', 'affiliation']

    # output fields
    # fields = ['type', 'number', 'doi', 'spage', 'epage', 'issue', 'partnum',
    #           'publication', 'year', 'rank', 'title', 'abstract', 'affiliation']

    out_paper = paper_row[:12] + [paper_row[14]]
    terms = paper_row[13].split('|')
    authors = paper_row[12].split('|')
    return out_paper, authors, terms


if __name__ == '__main__':
    infile = open('data.tsv', 'r')
    paperfile = open('papers.tsv', 'ta', newline='')
    termfile = open('terms.tsv', 'ta', newline='')
    authorfile = open('authors.tsv', 'ta', newline='')

    raw_reader = csv.reader(infile, delimiter='\t')
    paper_writer = csv.writer(paperfile, delimiter='\t')
    term_writer = csv.writer(termfile, delimiter='\t')
    author_writer = csv.writer(authorfile, delimiter='\t')

    count = 0
    for paper_row in raw_reader:
        count += 1
        outpaper, authors, terms = extract_one_paper(paper_row)
        paper_writer.writerow([count] + outpaper)
        for term in terms:
            if len(term.strip()) > 0:
                term_writer.writerow([count, term])
        for author in authors:
            if len(author.strip()) > 0:
                author_writer.writerow([count, author])

    infile.close()
    paperfile.close()
    termfile.close()
    authorfile.close()
