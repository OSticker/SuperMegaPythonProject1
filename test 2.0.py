import sqlite3

conn = sqlite3.connect('sql_test.db')
bd = conn.cursor()
bd.execute("""CREATE TABLE IF NOT EXISTS users(
   id INT PRIMARY KEY,
   name TEXT,
   color LIST);
""")
bd.execute("""INSERT INTO users(id, name, color) 
   VALUES('sdf', 'Одежда', [Коричневый]);""")
conn.commit()
bd.execute("SELECT * FROM users;")
three_results = bd.fetchmany(5)
conn.commit()
print(three_results)