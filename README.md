# Shelf Tracker

A Python command-line application for managing a small bookstore inventory with SQLite. Users can add, update, delete, and search books through an interactive terminal menu, with inventory saved between sessions.

This portfolio project demonstrates CRUD operations, parameterized SQL queries, relational tables, joins, and basic input validation.

## Technologies

- Python 3
- SQLite through Python's built-in `sqlite3` module
- SQL: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, and `INNER JOIN`

No third-party Python packages are required. The application creates its local database automatically.

## Features

- Add books with a book ID, title, author, author ID, author country, and stock quantity.
- Update book quantities and titles, or change an author's name and country.
- Delete a book by its ID.
- Search by book ID or a partial title, displaying author information and stock quantity.
- View titles and author details for all books.
- Store book and author information in separate tables linked through `authorID`.
- Populate the database with five sample books and five sample authors.
- Handle invalid menu input and SQLite errors through terminal messages.

## Getting started

### 1. Download the project

With Git installed, clone the repository and enter its directory:

```bash
git clone https://github.com/650buxks/shelf-tracker.git
cd shelf-tracker
```

Alternatively, use GitHub's **Code > Download ZIP** option, extract the files, and open a terminal in the directory containing `Shelf_track.py`.

### 2. Run the application

```bash
python3 Shelf_track.py
```

On Windows, use `py Shelf_track.py` if the Python launcher is installed.

On startup, the application creates `ebookstore.db` in the current working directory, creates the required tables, and inserts any missing sample records. Run the script from the same directory each time to use the same database.

## Menu options

| Option | Action |
| --- | --- |
| `1` | Enter a new book and its author details |
| `2` | Update a book's quantity, title, or author details |
| `3` | Delete a book by ID |
| `4` | Search by book ID or partial title |
| `5` | View titles and author details for all books |
| `0` | Exit the application |

Within the update menu, enter `1` for quantity, `2` for title, or `3` for author name and country. Any other update choice also takes the quantity-update path in the current implementation.

### Example: search the sample inventory

1. Start the application.
2. Enter `4` to search.
3. Enter `3001` as the book ID.

The application displays the sample record for **A Tale of Two Cities**, including its author, country, and current stock. You can also search for a partial title such as `Alice`.

## Database structure

### `book` table

| Column | Declared type | Purpose |
| --- | --- | --- |
| `id` | `INT PRIMARY KEY` | Book identifier |
| `title` | `TEXT` | Book title |
| `authorID` | `INTEGER` | Links the book to an author record |
| `qty` | `INTEGER` | Stock quantity |

### `author` table

| Column | Declared type | Purpose |
| --- | --- | --- |
| `id` | `INT PRIMARY KEY` | Author identifier |
| `name` | `TEXT` | Author name |
| `country` | `TEXT` | Author country |

The application joins `book.authorID` to `author.id` when displaying and searching records. This relationship is used in queries but is not enforced by a database foreign-key constraint.

## Project files

| File | Purpose |
| --- | --- |
| `Shelf_track.py` | Database initialization, menu, and inventory operations |
| `ebookstore.db` | Local SQLite database created when the application runs |
| `.gitignore` | Excludes the local database, Python cache files, and macOS metadata |

The local database is excluded from version control. A fresh download creates its own sample inventory.

## Current limitations

- **ID and quantity validation:** New book and author IDs are checked for a length of four characters, but the code does not verify that every character is a digit. Quantities must parse as integers, but negative values are accepted.
- **Sample records return on startup:** Sample records use `INSERT OR IGNORE` on every launch. Deleting a sample book removes it for the current session, but the record is restored the next time the application starts. User-added books are not recreated this way.
- **Shared author records:** Updating an author's name or country affects every book linked to that author ID. Adding a book with an existing author ID retains the author details already stored in the database.
- **Deletion feedback:** The application prints a deletion message even when the supplied book ID does not match a record.

## Future improvements

- Validate numeric IDs, nonnegative quantities, and update-menu choices.
- Separate sample-data initialization from normal startup.
- Enforce book-to-author relationships with foreign-key constraints.
- Check whether a book exists and request confirmation before deletion.
- Add automated tests for inventory operations and invalid input.
- Add a stock-summary view and low-stock filtering.

## Author

**Francis Isip**

- [GitHub](https://github.com/650buxks)
- [Portfolio](https://650buxks.github.io/MyCV/)
