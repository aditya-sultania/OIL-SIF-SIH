from src.db import get_connection, init_db
try:
 c=get_connection(); print('MySQL connection successful!'); c.close(); init_db(); print('Database/table initialization successful!')
except Exception as e: print('MySQL connection failed:'); print(e)
