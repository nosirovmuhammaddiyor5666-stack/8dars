Drop table if exists books;


CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    price INTEGER NOT NULL,
    quantity INTEGER NOT NULL
);

INSERT INTO books (title, author, price, quantity)
VALUES
    ('O''tkan kunlar', 'Abdulla Qodiriy', 40000, 3),
    ('Mehrobdan chayon', 'Abdulla Qodiriy', 35000, 5),
    ('Sariq devni minib', 'Xudoyberdi To''xtaboyev', 30000, 2),
    ('Shum bola', 'G''afur G''ulom', 25000, 4),
    ('Dunyoning ishlari', 'O''tkir Hoshimov', 45000, 6);

SELECT * FROM books;


