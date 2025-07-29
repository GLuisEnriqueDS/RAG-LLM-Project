import sqlite3

# Crear base de datos
conn = sqlite3.connect("netflix.db")
cur = conn.cursor()

# Tabla Gender
cur.execute("""
CREATE TABLE Gender (
    genderID INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
""")
cur.executemany("INSERT INTO Gender VALUES (?, ?)", [
    (1, "Action"),
    (2, "Adventure"),
    (3, "Drama"),
    (4, "Comedy"),
    (5, "Thriller"),
    (6, "Sci-Fi"),
    (7, "Horror"),
    (8, "Romance"),
    (9, "Documentary"),
    (10, "Animation")
])

# Tabla Movie
cur.execute("""
CREATE TABLE Movie (
    movieID TEXT PRIMARY KEY,
    movieTitle TEXT NOT NULL,
    releaseDate TEXT NOT NULL,
    originalLanguage TEXT NOT NULL,
    link TEXT
)
""")
cur.executemany("INSERT INTO Movie VALUES (?, ?, ?, ?, ?)", [
    ("80192187", "Triple Frontier", "2019-04-12", "English", "https://www.netflix.com/title/80192187"),
    ("81157374", "Run", "2021-05-21", "English", "https://www.netflix.com/title/81157374"),
    ("80210920", "The Mother", "2023-01-05", "English", "https://www.netflix.com/title/80210920"),
    ("70005379", "Pulp Fiction", "1994-10-14", "English", "https://www.netflix.com/title/70005379"),
    ("80050063", "Roma", "2018-11-21", "Spanish", "https://www.netflix.com/title/80050063"),
    ("80117401", "Bird Box", "2018-12-14", "English", "https://www.netflix.com/title/80117401"),
    ("80002479", "The Irishman", "2019-11-01", "English", "https://www.netflix.com/title/80002479"),
    ("80990668", "Parasite", "2019-05-30", "Korean", "https://www.netflix.com/title/80990668"),
    ("80118941", "Marriage Story", "2019-12-06", "English", "https://www.netflix.com/title/80118941"),
    ("80057281", "Inside Out", "2015-06-19", "English", "https://www.netflix.com/title/80057281")
])

# Tabla Movie_Gender
cur.execute("""
CREATE TABLE Movie_Gender (
    movieID TEXT,
    genderID INTEGER,
    PRIMARY KEY (movieID, genderID),
    FOREIGN KEY (movieID) REFERENCES Movie(movieID),
    FOREIGN KEY (genderID) REFERENCES Gender(genderID)
)
""")
cur.executemany("INSERT INTO Movie_Gender VALUES (?, ?)", [
    ("80192187", 1),
    ("80192187", 2),
    ("81157374", 5),
    ("80210920", 1),
    ("70005379", 3),
    ("70005379", 4),
    ("80050063", 3),
    ("80117401", 7),
    ("80002479", 1),
    ("80002479", 3),
    ("80990668", 5),
    ("80990668", 3),
    ("80118941", 3),
    ("80118941", 8),
    ("80057281", 10),
    ("80057281", 8)
])

# Tabla Country
cur.execute("""
CREATE TABLE Country (
    countryID INTEGER PRIMARY KEY,
    countryName TEXT UNIQUE NOT NULL
)
""")
cur.executemany("INSERT INTO Country VALUES (?, ?)", [
    (1, "USA"),
    (2, "Mexico"),
    (3, "Canada"),
    (4, "South Korea"),
    (5, "France"),
    (6, "Germany"),
    (7, "Italy"),
    (8, "Spain"),
    (9, "UK"),
    (10, "Brazil")
])

# Tabla Person
cur.execute("""
CREATE TABLE Person (
    personID TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    birthday TEXT,
    countryID INTEGER,
    FOREIGN KEY (countryID) REFERENCES Country(countryID)
)
""")
cur.executemany("INSERT INTO Person VALUES (?, ?, ?, ?)", [
    ("72129839", "Joseph Chavez Pineda", "1997-04-12", 1),
    ("73235434", "Aria Lopez Gutierrez", "1987-05-21", 2),
    ("20432364", "Maria Alejandra Navarro", "1967-01-05", 3),
    ("12345678", "Quentin Tarantino", "1963-03-27", 1),
    ("87654321", "Alfonso Cuarón", "1961-11-28", 2),
    ("11223344", "Sandra Bullock", "1964-07-26", 1),
    ("55667788", "Robert De Niro", "1943-08-17", 1),
    ("99887766", "Bong Joon-ho", "1969-09-14", 4),
    ("44332211", "Scarlett Johansson", "1984-11-22", 1),
    ("66778899", "Amy Poehler", "1971-09-16", 1)
])

# Tabla Participant
cur.execute("""
CREATE TABLE Participant (
    movieID TEXT,
    personID TEXT,
    participantRole TEXT,
    PRIMARY KEY (movieID, personID),
    FOREIGN KEY (movieID) REFERENCES Movie(movieID),
    FOREIGN KEY (personID) REFERENCES Person(personID)
)
""")
cur.executemany("INSERT INTO Participant VALUES (?, ?, ?)", [
    ("80192187", "72129839", "Actor"),
    ("81157374", "73235434", "Director"),
    ("80210920", "20432364", "Actor"),
    ("70005379", "12345678", "Director"),
    ("80050063", "87654321", "Director"),
    ("80117401", "11223344", "Actor"),
    ("80002479", "55667788", "Actor"),
    ("80990668", "99887766", "Director"),
    ("80118941", "44332211", "Actor"),
    ("80057281", "66778899", "Voice Actor")
])

# Tabla Award
cur.execute("""
CREATE TABLE Award (
    awardID INTEGER PRIMARY KEY AUTOINCREMENT,
    movieID TEXT NOT NULL,
    awardName TEXT NOT NULL,
    rating REAL NOT NULL,
    FOREIGN KEY (movieID) REFERENCES Movie(movieID)
)
""")
cur.executemany("INSERT INTO Award (movieID, awardName, rating) VALUES (?, ?, ?)", [
    ("80192187", "Best Action Movie", 4.5),
    ("81157374", "Best Director", 4.0),
    ("80210920", "Best Actress", 4.8),
    ("70005379", "Best Original Screenplay", 4.9),
    ("80050063", "Best Cinematography", 4.7),
    ("80117401", "Best Horror Film", 4.2),
    ("80002479", "Lifetime Achievement", 4.8),
    ("80990668", "Best International Film", 5.0),
    ("80118941", "Best Ensemble Cast", 4.6),
    ("80057281", "Best Animated Film", 4.9)
])

# Guardar y cerrar
conn.commit()
conn.close()
