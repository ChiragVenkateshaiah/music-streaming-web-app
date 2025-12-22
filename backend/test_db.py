from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:admin@localhost:5432/music_app"
)

try:
    with engine.connect() as conn:
        print(" Database connection successful")

except Exception as e:
    print("Database connection failed")
    print(e)