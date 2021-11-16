import sqlite3

conn = sqlite3.connect('sql_test.db')
bd = conn.cursor()
bd.execute("""CREATE TABLE IF NOT EXISTS users(
   id INT PRIMARY KEY,
   name TEXT,
   color TEXT);
""")
conn.commit()
a = '1'
bd.execute("""INSERT INTO users(id, name, color) 
   VALUES('a', 'Одежда', 'Коричневый');""")
conn.commit()
conn2 = sqlite3.connect(str(a) + '.db')
bd2 = conn2.cursor()
bd2.execute("""CREATE TABLE IF NOT EXISTS users(
   id INT PRIMARY KEY,
   name TEXT,
   kolvo INTEGER);
""")
bd2.execute("""INSERT INTO users(id, name, kolvo) 
   VALUES('1', 'Шуба', '5');""")

bd.execute("SELECT * FROM users;")
three_results = bd.fetchmany(5)
bd2.execute("SELECT * FROM users;")
three = bd2.fetchmany(5)
print(three_results, three, sep='\n')

