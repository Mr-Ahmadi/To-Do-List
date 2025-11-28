# test_sqlalchemy.py
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://todouser:todopass@localhost:5432/todolist_db"

try:
    engine = create_engine(DATABASE_URL, echo=True)
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ SQLAlchemy connection موفق!")
        
        # بررسی user و database
        db_info = conn.execute(text("""
            SELECT current_database(), current_user;
        """)).fetchone()
        
        print(f"📊 Database: {db_info[0]}")
        print(f"👤 User: {db_info[1]}")
        
except Exception as e:
    print(f"❌ خطا: {e}")
    import traceback
    traceback.print_exc()
