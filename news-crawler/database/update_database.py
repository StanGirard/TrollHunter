import sqlite3

conn = sqlite3.connect('trollhunter.db')
print ("Opened database successfully")

cursor = conn.execute("SELECT id, url_provider, site_map_path from NEWS_PROVIDERS")
for row in cursor:
    parse_sitemap(row[1]+row[2], ["loc", "lastmod"])

print("Operation done successfully")
conn.close()