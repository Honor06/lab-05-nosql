#!/usr/bin/env python3
import logging
import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError

MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

# Configure logging to report connection status and errors.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    """Connect to MongoDB and print selected authors and their linked books."""

    # Include at least one author added in step 7 and one from the loaded files.
    # Replace these example IDs with actual author _id values from your database.
    author_ids = [
        "author_003",
	    "author_004",
        "author_005",
    ]

    client = None

    try:
        # Verify that the required environment variables are configured.
        if not all([
            MONGODB_ATLAS_URL,
            MONGODB_ATLAS_USER,
            MONGODB_ATLAS_PWD,
        ]):
            logging.error("MongoDB Atlas environment variables are missing.")
            return

        # Connect using the URL and credentials supplied by the environment.
        client = MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
            serverSelectionTimeoutMS=10000,
        )

        # Verify connectivity before querying the database.
        client.admin.command("ping")
        logging.info("Successfully connected to MongoDB Atlas.")

        # Select the bookstore database and required collections.
        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]

        # Count authors whose _id is included in the requested list.
        total_authors = authors.count_documents({"_id": {"$in": author_ids}})
        print(f"\nTotal authors in the requested list: {total_authors}")

        # Look up each author and list books linked through their author IDs.
        for author_id in author_ids:
            author = authors.find_one({"_id": author_id})

            if author is None:
                logging.warning("Author not found for ID: %s", author_id)
                continue

            author_name = author.get("name", "Unknown author")
            print(f"\nAuthor: {author_name}")
            print("-" * (len(author_name) + 8))

            # Adjust "authors" below if your book documents use a different
            # field name or store author IDs in another format.
            linked_books = books.find({"author_ids": author_id})

            book_found = False
            for book in linked_books:
                book_found = True
                title = book.get("title", "Untitled")
                published_year = book.get("published_year", "Unknown")
                print(f"  - {title} ({published_year})")

            if not book_found:
                print("  No linked books found.")

    except PyMongoError:
        # Log database errors without exposing credentials.
        logging.exception("A MongoDB operation failed.")

    except Exception:
        # Log unexpected errors with their traceback for debugging.
        logging.exception("An unexpected error occurred.")

    finally:
        # Always close the client if it was created.
        if client is not None:
            client.close()
            logging.info("MongoDB client closed.")


if __name__ == "__main__":
    # Run the report only when this file is executed directly.
    main()
