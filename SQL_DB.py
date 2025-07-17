import sqlite3
import pandas as pd

conn = sqlite3.connect("doctors.db")
df = pd.read_sql("SELECT * FROM doctors", conn)
print(df.head())  # or df.to_string(index=False) for full view
conn.close()


from faker import Faker
import random
import sqlite3

# Initialize Faker
fake = Faker()
Faker.seed(0)

# database schema
doctor_types = ["PT", "OT", "SLP"]
specialties = [
    "Stroke Rehab", "Autism", "Speech Delay", "Cognitive Rehab", 
    "Motor Skills Training", "Sensory Integration", "Post-Surgery Recovery",
    "Parkinson's Therapy", "Balance Issues", "Hand Therapy"
]
settings = ["In-home", "Clinic", "Telehealth"]
georgia_cities = [
    ("Roswell", "GA"), ("Atlanta", "GA"), ("Alpharetta", "GA"),
    ("Marietta", "GA"), ("Decatur", "GA"), ("Duluth", "GA"),
    ("Sandy Springs", "GA"), ("Johns Creek", "GA"),
    ("Norcross", "GA"), ("Lawrenceville", "GA"), ("Suwanee", "GA")
]

# Connect to SQLite and set up table
conn = sqlite3.connect("doctors.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        type TEXT,
        city TEXT,
        state TEXT,
        specialty TEXT,
        setting TEXT,
        address TEXT,
        contact_info TEXT
    )
''')

# Generate 200 fake entries
for _ in range(200):
    name = fake.name()
    doc_type = random.choice(doctor_types)
    city, state = random.choice(georgia_cities)
    specialty = random.choice(specialties)
    setting = random.choice(settings)
    address = fake.street_address() + f", {city}, {state}"
    contact = fake.email()

    cursor.execute('''
        INSERT INTO doctors (name, type, city, state, specialty, setting, address, contact_info)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, doc_type, city, state, specialty, setting, address, contact))

conn.commit()
conn.close()

print("✅ doctors.db created with 200 fake doctors")
