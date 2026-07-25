import pymysql

try:
    conn = pymysql.connect(
        host="sakura.proxy.rlwy.net",      # Public Host
        port=28273,                        # Public Port
        user="root",                       # Public User
        password="DgNAqNFlgJfHoOzYyXAeQjnBgmntUGjY",   # Replace with your Public Password
        database="railway",
        connect_timeout=10
    )

    print("✅ Connected Successfully!")

    cursor = conn.cursor()

    cursor.execute("SELECT DATABASE();")
    print("Current Database:", cursor.fetchone())

    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()

    if tables:
        print("\nTables in database:")
        for table in tables:
            print(table[0])
    else:
        print("\nNo tables found.")

    cursor.close()
    conn.close()

except Exception as e:
    print("\nConnection Failed!")
    print(e)