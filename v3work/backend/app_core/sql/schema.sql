CREATE DATABASE IF NOT EXISTS oil_sif;
USE oil_sif;
CREATE TABLE IF NOT EXISTS reports (id INT AUTO_INCREMENT PRIMARY KEY, report_id VARCHAR(100) UNIQUE, site VARCHAR(255), location VARCHAR(255), report_type VARCHAR(100), narrative TEXT NOT NULL, activity VARCHAR(255), hazard VARCHAR(500), sif_class VARCHAR(20), sif_probability DECIMAL(6,5), priority_score INT, life_saving_rule VARCHAR(500), barrier VARCHAR(255), barrier_failure TEXT, potential_consequence TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
