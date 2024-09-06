import sqlite3

# Create a connection object
conn = sqlite3.connect('mydatabase.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table
# cursor.execute('''CREATE TABLE songs
#                   (song_id integer primary key, artist text not null, name text not null)''')

# Insert data
# # cursor.execute("INSERT INTO songs VALUES (1, 'Taylor Swift', 'Love Story')")
# cursor.execute("INSERT INTO songs VALUES (2, 'Taylor Swift', 'You Belong With Me')")
# cursor.execute("INSERT INTO songs VALUES (3, 'Justin Bieber', 'Baby')")
# cursor.execute("INSERT INTO songs VALUES (4, 'Justin Bieber', 'Love Yourself')")
cursor.execute("INSERT INTO songs VALUES (5, 'Ed Sheeran', 'Shape of You')")
conn.commit()