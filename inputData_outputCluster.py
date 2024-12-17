
import psycopg2
conn = psycopg2.connect(database="postgres",
                    host="localhost",
                    user="bkaii",
                    password=",Interstellar123,"
                    )
# cursor = conn.cursor()
# print("Connected")

# query="SELECT..."
# cursor.execute(query)

# tuples = cursor.fetchall()

# print(tuples)

# conn.commit()
# conn.close()
# print("Connexion closed")