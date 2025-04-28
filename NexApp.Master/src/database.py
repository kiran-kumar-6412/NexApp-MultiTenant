from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.utils import logger
from src.config.config import settings  # Importing Pydantic settings


# Get database URL from Pydantic settings
DB_URL = settings.DATABASE_URL

# Debugging: Ensure DB_URL is loaded
if not DB_URL:
    raise ValueError("❌ Database URL is missing! Check your .env file.")

try:
    # Create database engine
    engine = create_engine(DB_URL)

    # Create session factory
    local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    logger.logging_error("✅ Database connected successfully!")  # Log successful connection
except Exception as e:
    logger.logging_error("Database Error", f"Database Connection Error: {str(e)}") # Log error
    
   