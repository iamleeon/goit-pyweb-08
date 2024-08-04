import json

from models import Author, Quote

if __name__ == "__main__":
    authors = "authors.json"
    quotes = "quotes.json"

    with open(authors, "r", encoding="utf-8") as f:
        authors_pool = json.load(f)
        for person in authors_pool:
            author = Author(fullname=person.get("fullname"), born_date=person.get("born_date"),
                            born_location=person.get("born_location"), description=person.get("description")).save()

    with open(quotes, "r", encoding="utf-8") as f:
        quotes_pool = json.load(f)
        for el in quotes_pool:
            quote = Quote(tags=el.get("tags"), author=author, quote=el.get("quote")).save()
