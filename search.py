import sys
import connect

from models import Author, Quote


sys.stdout.reconfigure(encoding="utf-8")


def search_by_author(name):
    author = Author.objects(fullname=name).first()
    if author:
        quotes = Quote.objects(author=author)
        return [quote.quote for quote in quotes]


def search_by_tag(tag):
    tag_list = tag.split(',')
    quotes = Quote.objects(tags__in=tag_list).distinct('quote')
    return quotes


def main():
    while True:
        command = input("Search by:\x1B[3m name: author\x1B[0m OR\x1B[3m tag: tag1\x1B[0m "
                        "OR \x1B[3mtags: tag1,tag2\x1B[0m\nType\x1B[3m exit\x1B[0m to quit.\n>>> ").strip()
        if command == "exit":
            print("Chao!")
            sys.exit(0)

        if command.startswith("name"):
            name = command[5:].strip()
            result = search_by_author(name)
            if result:
                for q in result:
                    print(f"{q}")
            else:
                print(f"No quotes found for {name}")

        if command.startswith("tag"):
            tags = command[4:].strip() if command.startswith("tag:") else command[5:].strip()
            results = search_by_tag(tags)
            if results:
                print(f"Quotes with tag(s) '{tags}':")
                for q in results:
                    print(f"{q}")
            else:
                print(f"No quotes found with tag(s): {tags}")


if __name__ == "__main__":
    main()
