import psycopg2


def connect_db():
    conn = psycopg2.connect(host='server.trollhunter.guru', database='sitemap', user='trollhunter', password='trollhunter')
    print('Connection database')
    return conn


def disconnect_db(conn, cur):
    if conn:
        cur.close()
        conn.close()
        print('Database connection closed')


def get_sitemap(id):
    conn = None
    cur = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = """select * from sitemap where id = %s"""
        cur.execute(query, (id,))
        data = cur.fetchone()
        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect_db(conn, cur)


def update_sitemap(id, data):
    conn = None
    cur = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = """update sitemap set last_loc = %s where id = %s"""
        cur.execute(query, (data, id))
        conn.commit()
        print('Update sitemap last_loc %s whth %s' % (id, data))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect_db(conn, cur)


def insert_sitemap(data):
    conn = None
    cur = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = """insert into sitemap values %s"""
        cur.execute(query, data.str)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect_db(conn, cur)
