import psycopg2

try :
    conn = psycopg2.connect(database="masterbook",
                        port="5433",
                        user="root",
                        host="localhost",
                        password="root"
                        )
except psycopg2.Error as e:
    conn = None
    print(e)