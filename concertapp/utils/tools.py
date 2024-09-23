from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Initialize Base for model classes
Base = declarative_base()
print("tools.py script is running...")

# Function to get an engine to the database
def get_engine(use_memory=False):
    if use_memory:
        return create_engine('sqlite:///:memory:', echo=False)  # In-memory DB for testing
    else:
        return create_engine('sqlite:///concerts.db', echo=False)  # Persistent DB

# Bind the engine to sessionmaker
engine = get_engine(use_memory=False)
SessionLocal = sessionmaker(bind=engine)

# Create the tables
def create_db():
    Base.metadata.create_all(engine)
    print("Database and tables created successfully.")

# Automatically create DB if this script is executed directly
if __name__ == "__main__":
    create_db()
