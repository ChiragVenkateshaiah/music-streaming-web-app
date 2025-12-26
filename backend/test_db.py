from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:music-streaming-app@db.cteoorioifetpeiidxuq.supabase.co:5432/postgres"
)

try:
    with engine.connect() as conn:
        print(" Database connection successful")

except Exception as e:
    print("Database connection failed")
    print(e)