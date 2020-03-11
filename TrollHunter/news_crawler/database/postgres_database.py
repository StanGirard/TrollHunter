import psycopg2


def connect_db():
    conn = psycopg2.connect(host='142.93.170.234', database='sitemap', user='trollhunter', password='trollhunter')
    return conn


def disconnect_db(conn, cur):
    if conn:
        cur.close()
        conn.close()


def get_sitemap_parent():
    conn = None
    cur = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = """select * from sitemap where lastmod is null"""
        cur.execute(query)
        data = cur.fetchall()
        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect_db(conn, cur)


def get_all_sitemap():
    conn = None
    cur = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = """select * from sitemap"""
        cur.execute(query)
        data = cur.fetchall()
        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect_db(conn, cur)


def get_sitemap(id):
    conn = None
    cur = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = """select * from sitemap where url = %s"""
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
        query = """update sitemap set lastmod = %s where url = %s"""
        cur.execute(query, (data, id))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect_db(conn, cur)


def insert_sitemap(loc, lasmod, url_headers, id_trust):
    conn = None
    cur = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = """insert into sitemap values (%s, %s, %s, %s)"""
        cur.execute(query, (loc, lasmod, url_headers, id_trust))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect_db(conn, cur)


def get_trust_levels():
    conn = None
    cur = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = """select * from trust_level"""
        cur.execute(query)
        data = cur.fetchall()
        return data
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect_db(conn, cur)
