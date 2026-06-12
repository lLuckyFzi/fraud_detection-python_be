import os

from sqlalchemy import text
from database import engine, Base

import models

def init_db():
    print("Initializing database and creating tables...")
    
    Base.metadata.create_all(bind=engine)

    print("Database initialized successfully.")

def apply_sql_scrips():
    with engine.connect() as connection:
        scripts = ["01_before_transaction.sql", "02_after_transaction.sql", "03_create_views.sql"]
        
        for script_name in scripts:
            filepath = os.path.join("sql_scripts", script_name)
            
            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    full_sql = f.read()
                    
                    commands = full_sql.split('-- SPLIT --')
                    
                    for cmd in commands:
                        cleaned_cmd = cmd.strip()
                        if cleaned_cmd:
                            connection.execute(text(cleaned_cmd))
                            
                print(f"-> File {script_name} berhasil dieksekusi.")
            else:
                print(f"-> Peringatan: File {script_name} tidak ditemukan.")
                
        connection.commit()

    print("Applied SQL scripts successfully.")

if __name__ == "__main__":
    init_db()
    apply_sql_scrips()