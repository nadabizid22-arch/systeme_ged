import oracledb

# Initialisation du client Oracle (chemin où se trouve ton Instant Client)
oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient-basic-windows.x64-19.28.0.0.0dbru\instantclient_19_28")

# Connexion à la base Oracle
def get_connection():
    return oracledb.connect(
        user="ged_user",
        password="ged_password",
        dsn="localhost/XE"
    )
