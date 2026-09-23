"""Manage a small bookstore inventory using SQLite."""

import sqlite3

with sqlite3.connect('ebookstore.db') as db:
    cursor = db.cursor()

    # Create the book table.
    cursor.execute('''CREATE TABLE IF NOT EXISTS book(
        id INT PRIMARY KEY, title TEXT, authorID INTEGER, qty INTEGER)''')

    # Create the author table.
    cursor.execute('''CREATE TABLE IF NOT EXISTS author(
        id INT PRIMARY KEY, name TEXT, country TEXT)''')

    cursor.execute('''INSERT OR IGNORE INTO book (id, title, authorID, qty)
        VALUES
        (3001, "A Tale of Two Cities", 1290, 30),
        (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
        (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
        (3004, "The Lords of the Rings", 6380, 37),
        (3005, "Alice's Adventures in Wonderland", 5620, 12)''')

    cursor.execute('''INSERT OR IGNORE INTO author (id, name, country)
        VALUES
        (1290, 'Charles Dickens', 'England'),
        (8937, 'J.K. Rowling', 'England'),
        (2356, 'C.S. Lewis', 'Ireland'),
        (6380, 'J.R.R. Tolkien', 'South Africa'),
        (5620, 'Lewis Carroll', 'England')''')
    db.commit()

    def add_book():
        """Add a book and its author to the database."""
        try:
            book_id = input("Enter 4-digit Book ID: ")
            title = input("Enter Book Title: ")
            new_author = input("Enter Book's Author: ")
            author_id = input("Enter 4-digit Author ID: ")
            author_country = input("Enter author's country: ")
            qty = int(input("Enter Quantity: "))

            if len(book_id) != 4 or len(author_id) != 4:
                print("Error: ID must be exactly 4 digits long.")
                return

            cursor.execute('''
                INSERT INTO book (id, title, authorID, qty)
                VALUES (?, ?, ?, ?)
                ''', (book_id, title, author_id, qty))

            cursor.execute('''
                INSERT OR IGNORE INTO author (id, name, country)
                VALUES (?, ?, ?)
                ''', (author_id, new_author, author_country))

            db.commit()
            print(f"""
---- BOOK ADDED SUCCESSFULLY ----
Title:    {title}
BookId:   {book_id}
Author:   {new_author}
AuthorID: {author_id}
Country:  {author_country}
Quantity: {qty}
--------------------------------
        """)
        except ValueError:
            print("Error: QUANTITY and IDs must be numbers.")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def update_book():
        """Update a book's title, author, or quantity."""
        try:
            search_id = input("Enter 4-digit Book ID to search book: ")

            cursor.execute('''
                SELECT book.title, author.name, author.country,
                       book.qty, book.authorID
                FROM book
                INNER JOIN author on book.authorID = author.id
                WHERE book.id = ?
            ''', (search_id,))

            result = cursor.fetchone()

            if result:
                title, auth_name, auth_country, qty, auth_id = result
                print(
                    f"\nCurrent Details:\nTitle: {title}\n"
                    f"Author: {auth_name} ({auth_country})\nQuantity: {qty}"
                )

                print("\nWhat would you like to update?")
                print("1. Quantity (Default)")
                print("2. Title")
                print("3. Author Name/Country")
                choice = input("Enter choice (1-3): ")

                if choice == '2':
                    new_title = input("Enter new title: ")
                    cursor.execute('''
                        UPDATE book
                        SET title = ?
                        WHERE id = ?
                    ''', (new_title, search_id))
                elif choice == '3':
                    new_name = input("Enter new author name: ")
                    new_country = input("Enter new country: ")
                    cursor.execute('''
                        UPDATE author
                        SET name = ?,
                        country = ?
                        WHERE id = ?
                    ''', (new_name, new_country, auth_id))
                else:
                    new_qty = int(input("Enter new quantity: "))
                    cursor.execute('''
                        UPDATE BOOK
                        SET qty = ?
                        WHERE id = ?
                        ''', (new_qty, search_id))

                db.commit()
                print("Update successful!")
            else:
                print("Book ID not found")

        except ValueError:
            print("Error: Enter valid Book ID")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def delete_book():
        """Delete a book from the database."""
        try:
            book_id = input("Enter 4-digit Book ID to delete book info: ")

            cursor.execute('''
                DELETE from book
                WHERE id = ?
            ''', (book_id,))

            db.commit()
            print("Book info deleted")

        except ValueError:
            print("Error: Enter valid Book ID")
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def search_book():
        """Search for books by ID or title."""
        try:
            book_search = input("Enter 4-digit Book ID or Title:")
            cursor.execute('''
                SELECT book.id, book.title, author.name,
                       author.country, book.qty
                FROM book
                INNER JOIN author ON book.authorID = author.id
                where book.id = ? OR book.title LIKE ?
            ''', (book_search, f'%{book_search}%'))

            results = cursor.fetchall()

            if results:
                print("\n--- SEARCH RESULTS ---")
                for row in results:
                    book_id, title, author, country, qty = row
                    print(f"ID: {book_id} | Title: {title}")
                    print(f"Author: {author} | ({country})")
                    print(f"Current Stock: {qty}")
                    print("-" * 25)
            else:
                print(f"No results found for '{book_search}'.")

        except sqlite3.Error as e:
            print(f"Database Error: {e}")

    def view_details():
        """Display the title and author details for every book."""
        try:
            cursor.execute('''
                SELECT book.title, author.name, author.country
                FROM book
                INNER JOIN author on book.authorID = author.id
            ''')

            all_books = cursor.fetchall()

            if all_books:
                print("\n--- FULL BOOKSTORE INVENTORY ---")
                for book in all_books:
                    title, name, country = book
                    print(f"Title: {title}")
                    print(f"Author's Name: {name}")
                    print(f"Author's country: {country}")
                    print("-" * 30)
            else:
                print("The database is currently empty")

        except sqlite3.Error as e:
            print(f"Database error: {e}")

    # Show the user menu.
    while True:
        try:
            menu = int(input('''
Select one of the options:
1. Enter book
2. Update book
3. Delete book
4. Search books
5. View details of all books
0. Exit
                 '''))

            if menu == 1:
                add_book()
            elif menu == 2:
                update_book()
            elif menu == 3:
                delete_book()
            elif menu == 4:
                search_book()
            elif menu == 5:
                view_details()
            elif menu == 0:
                print("Goodbye!!!")
                break
            else:
                print("You have entered an invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number. ")
