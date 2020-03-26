import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

def connect_db():
    conn = psycopg2.connect(host=os.getenv("SQL_SERVER"), database=os.getenv("SQL_DATABASE"), user=os.getenv("SQL_USER"), password=os.getenv("SQL_PASSWORD"))
    return conn


def disconnect_db(conn, cur):
    if conn:
        cur.close()
        conn.close()


def get_sitemap_parent():
    """
    Retrieve sitemaps where the date of last modification is null.
    Sitemaps with lastmod null are the root of the sitemap tree of a website.

    :return: list of root sitemaps
    """
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
    """
    Request all sitemaps.

    :return: list of all sitemaps
    """
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
    """
    Request a specific sitemap with its url.

    :param id: url of the sitemap
    :return: the sitemap if present, None otherwise
    """
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
    """
    Update the date of last modification of a sitemap.

    :param id: url of the sitemap
    :param data: new date of last modification
    """
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


def insert_sitemap(loc, lastmod, url_headers, id_trust):
    """
    Insert a new sitemap in the database.

    :param loc: url of the sitemap
    :param lastmod: date of last modification of the sitemap, None if root sitemap
    :param url_headers: xml tags to retrieve in the content of the sitemap in the url tag
    :param id_trust: id of the trust level in the news website
    """
    conn = None
    cur = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = """insert into sitemap values (%s, %s, %s, %s)"""
        cur.execute(query, (loc, lastmod, url_headers, id_trust))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        disconnect_db(conn, cur)


def get_trust_levels():
    """
    Retrieve all trust levels with their id and label.

    :return: list of trust levels
    """
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
