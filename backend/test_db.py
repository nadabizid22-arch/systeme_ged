import oracledb

# Indique le chemin exact où se trouve oci.dll
oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient-basic-windows.x64-19.28.0.0.0dbru\instantclient_19_28")

username = "ged_user"
password = "ged_password"
dsn = "localhost/XE"

connection = oracledb.connect(user=username, password=password, dsn=dsn)
cursor = connection.cursor()

cursor.execute("""
    INSERT INTO ged_documents (original_name, storage_path, content_type, size_bytes, created_by)
    VALUES (:1, :2, :3, :4, :5)
""", ("test.pdf", "/documents/test.pdf", "application/pdf", 1024, "admin"))

connection.commit()
print("✅ Document inséré avec succès !")

cursor.execute("SELECT doc_id, original_name FROM ged_documents")
for row in cursor:
    print(row)

cursor.close()
connection.close()
