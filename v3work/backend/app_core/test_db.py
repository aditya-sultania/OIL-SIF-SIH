import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Lira&&2006",  # <--- Change this to your actual password!
        database="oil_sif"
    )

    if connection.is_connected():
        print("--------------------------------------------------")
        print("⚡ Success! Python successfully connected to MySQL!")
        print("--------------------------------------------------")
        connection.close()

except mysql.connector.Error as err:
    print(f"❌ Connection failed with error: {err}")