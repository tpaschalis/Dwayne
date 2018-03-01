import sqlite3
import os.path

if os.path.exists('dwayne.db'):
    print("Database with the same name already exists!")
else:
    conn = sqlite3.connect('dwayne.db')
    c = conn.cursor()
    
    c.execute("""CREATE TABLE standups
            (uid text, 
            isodate text,
            mboxdate text,
            sender text,
            recipient text,
            subject text,
            answ1 text,
            answ2 text,
            answ3 text,
            mentions blob,
            team blob,
            task blob,
            hours blob) 
            """)

    conn.commit()
    conn.close()
