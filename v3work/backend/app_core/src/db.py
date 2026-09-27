import os, mysql.connector, pandas as pd
from dotenv import load_dotenv
load_dotenv()
def get_connection(): return mysql.connector.connect(host=os.getenv('DB_HOST','localhost'),port=int(os.getenv('DB_PORT','3306')),user=os.getenv('DB_USER','root'),password=os.getenv('DB_PASSWORD',''),database=os.getenv('DB_NAME','oil_sif'))
def init_db():
 c=get_connection(); cur=c.cursor(); cur.execute('''CREATE TABLE IF NOT EXISTS reports (id INT AUTO_INCREMENT PRIMARY KEY, report_id VARCHAR(100) UNIQUE, site VARCHAR(255), location VARCHAR(255), report_type VARCHAR(100), narrative TEXT NOT NULL, activity VARCHAR(255), hazard VARCHAR(500), sif_class VARCHAR(20), sif_probability DECIMAL(6,5), priority_score INT, life_saving_rule VARCHAR(500), barrier VARCHAR(255), barrier_failure TEXT, potential_consequence TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'''); c.commit(); cur.close(); c.close()
def save_report(narrative,r,report_id='',site='Unknown',location='Unknown',report_type='Unknown'):
 c=get_connection(); cur=c.cursor(); cur.execute('''INSERT INTO reports(report_id,site,location,report_type,narrative,activity,hazard,sif_class,sif_probability,priority_score,life_saving_rule,barrier,barrier_failure,potential_consequence) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(report_id or None,site,location,report_type,narrative,r['activity'],r['hazard'],r['sif_class'],r['sif_probability'],r['priority_score'],', '.join(r['life_saving_rules']),r['barrier'],r['barrier_failure'],r['potential_consequence'])); c.commit(); cur.close(); c.close()
def get_reports():
 c=get_connection(); df=pd.read_sql('SELECT * FROM reports ORDER BY created_at DESC',c); c.close(); return df
