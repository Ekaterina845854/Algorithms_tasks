# O(n*m) - где n - кол-во авторов, m - кол-во книг
def bruteforce(book_title, books, authors):
    for book in books:
        if book["title"] == book_title:
            author_id = book["author_id"]
            for author in authors:
                if author["author_id"] == author_id:
                    return author["name"]
    return None

# O(n+m)
def hashdict(book_title, books, authors):
    author_dict = {author["author_id"]: author["name"] for author in authors}

    for book in books:
        if book["title"] == book_title:
            return author_dict.get(book["author_id"], None)

    return None
