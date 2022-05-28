# Jimin: Alejandro Alonso (PM), Noakai Aronesty, Justin Zou, Ivan Lam
# SoftDev pd2
# P04 -- Smithy

""" Creation of db """

import sqlite3
from notanorm import SqliteDb

DB_FILE = "project_reviewal.db"

''' Creates / Connects to DB File '''

db = SqliteDb(DB_FILE)
db.query("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, stuy_username TEXT, password TEXT, firstname TEXT, lastname TEXT, github TEXT, devo_status TEXT);")
db.query("CREATE TABLE IF NOT EXISTS projects (project_id INTEGER PRIMARY KEY AUTOINCREMENT, project_title TEXT, author_ids TEXT, rating INTEGER);")
db.query("CREATE TABLE IF NOT EXISTS comments (comment TEXT, project_id INTEGER, upvotes INTEGER, downvotes INTEGER, anonymous INTEGER);")
db.query(
    "CREATE TABLE IF NOT EXISTS ratings (project_id INTEGER, user_id INTEGER, rating INTEGER);")
db.query(
    "CREATE TABLE IF NOT EXISTS favorites (user_id INTEGER, project_id INTEGER);")

db.close()

# For testing purposes #################

# db = sqlite3.connect(DB_FILE)
# c = db.cursor()
# c.execute("SELECT usernames FROM users")
# users = []
# for a_tuple in c.fetchall():
#     users.append(a_tuple[0])
# print(users)
