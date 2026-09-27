import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Lira&&2006",  # <--- Change this!
    database="oil_sif"
)

cursor = db.cursor()

# 1. Sites Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sites (
    site_id INT AUTO_INCREMENT PRIMARY KEY,
    site_name VARCHAR(100) NOT NULL,
    location VARCHAR(100)
);
""")

# 2. Life Saving Rules Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS life_saving_rules (
    rule_id INT AUTO_INCREMENT PRIMARY KEY,
    rule_name VARCHAR(100) NOT NULL,
    description TEXT
);
""")

# 3. Reports Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    report_id INT AUTO_INCREMENT PRIMARY KEY,
    report_date DATE,
    site_id INT,
    category VARCHAR(50), -- Unsafe Act, Unsafe Condition, Near Miss, Incident
    description TEXT,
    rule_id INT,
    FOREIGN KEY (site_id) REFERENCES sites(site_id),
    FOREIGN KEY (rule_id) REFERENCES life_saving_rules(rule_id)
);
""")

print("--------------------------------------------------")
print("🎉 All database tables created successfully!")
print("--------------------------------------------------")

cursor.close()
db.close()