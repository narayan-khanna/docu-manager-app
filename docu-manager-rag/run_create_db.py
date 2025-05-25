import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Import Base AFTER setting up Python path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models import Base

engine = create_engine(os.getenv("DATABASE_URL"))
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
