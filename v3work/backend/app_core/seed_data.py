import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Lira&&2006",  # <--- Change this!
    database="oil_sif"
)
cursor = db.cursor()

# Insert Sample Sites
sites_data = [
    ('Offshore Rig Alpha', 'North Sea'),
    ('Refinery Plant B', 'Texas, USA'),
    ('Pipeline Hub C', 'Alberta, Canada')
]
cursor.executemany("INSERT INTO sites (site_name, location) VALUES (%s, %s);", sites_data)

# Insert Sample Life Saving Rules
rules_data = [
    ('Bypassing Safety Controls', 'Obtain authorization before bypassing safety controls'),
    ('Work Authorization', 'Work with a valid work permit when required'),
    ('Confined Space', 'Obtain authorization before entering a confined space')
]
cursor.executemany("INSERT INTO life_saving_rules (rule_name, description) VALUES (%s, %s);", rules_data)

# Insert Sample Reports
reports_data = [
    ('2026-08-01', 1, 'Unsafe Act', 'Operator worked without wearing safety harness.', 1),
    ('2026-08-05', 2, 'Unsafe Condition', 'Oil leak detected on pressure valve valve #4.', 2),
    ('2026-08-10', 1, 'Near Miss', 'Crane hook swung close to walkways during lift.', 2),
    ('2026-08-15', 3, 'Incident', 'Minor chemical splash during pipe transfer.', 3),
    ('2026-08-20', 2, 'Unsafe Act', 'Worker entered storage silo without permit.', 3)
]
cursor.executemany("INSERT INTO reports (report_date, site_id, category, description, rule_id) VALUES (%s, %s, %s, %s, %s);", reports_data)

db.commit()
print("--------------------------------------------------")
print("🎉 Sample safety data successfully inserted!")
print("--------------------------------------------------")

cursor.close()
db.close()