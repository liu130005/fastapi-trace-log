## app/db/session.py
"""
Database session management for the AI Middleware Platform.

This module provides session management for both PostgreSQL (via SQLAlchemy)
and MongoDB databases, handling connection pooling, session creation, and
proper resource cleanup.
"""

from typing import Generator, Optional
from contextlib import contextmanager
import pymongo
from pymongo import MongoClient
from pymongo.database import Database as MongoDatabase
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine

from app.core.config import config


# Base class for SQLAlchemy models
Base = declarative_base()


class DatabaseManager:
    """Manages database connections and sessions for both PostgreSQL and MongoDB."""
    
    def __init__(self) -> None:
        """Initialize database managers for both PostgreSQL and MongoDB."""
        # PostgreSQL setup
        self._postgresql_engine: Optional[Engine] = None
        self._postgresql_session_local: Optional[sessionmaker] = None
        
        # MongoDB setup
        self._mongodb_client: Optional[MongoClient] = None
        self._mongodb_database: Optional[MongoDatabase] = None
        
        self._initialize_postgresql()
        self._initialize_mongodb()
    
    def _initialize_postgresql(self) -> None:
        """Initialize PostgreSQL connection and session factory."""
        self._postgresql_engine = create_engine(
            config.database_url,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=10,
            max_overflow=20
        )
        self._postgresql_session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._postgresql_engine
        )
    
    def _initialize_mongodb(self) -> None:
        """Initialize MongoDB connection and database reference."""
        self._mongodb_client = MongoClient(
            config.mongodb_url,
            connect=False,  # Lazy connection
            maxPoolSize=100,
            minPoolSize=10
        )
        # Extract database name from URL
        database_name = config.mongodb_url.split('/')[-1]
        if not database_name or database_name.startswith('?'):
            database_name = 'ai_middleware'
        self._mongodb_database = self._mongodb_client[database_name]
    
    @contextmanager
    def get_postgresql_session(self) -> Generator[Session, None, None]:
        """
        Create a context manager for PostgreSQL database sessions.
        
        Yields:
            Session: A SQLAlchemy database session.
        """
        if not self._postgresql_session_local:
            raise RuntimeError("PostgreSQL session factory not initialized")
        
        session = self._postgresql_session_local()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_mongodb_database(self) -> MongoDatabase:
        """
        Get the MongoDB database instance.
        
        Returns:
            MongoDatabase: The MongoDB database instance.
        
        Raises:
            RuntimeError: If MongoDB is not initialized.
        """
        if not self._mongodb_database:
            raise RuntimeError("MongoDB database not initialized")
        return self._mongodb_database
    
    def close_connections(self) -> None:
        """Close all database connections."""
        # Close PostgreSQL connections
        if self._postgresql_engine:
            self._postgresql_engine.dispose()
        
        # Close MongoDB connections
        if self._mongodb_client:
            self._mongodb_client.close()
    
    def create_postgresql_tables(self) -> None:
        """
        Create all tables defined in the SQLAlchemy models.
        
        This should be called during application startup.
        """
        if not self._postgresql_engine:
            raise RuntimeError("PostgreSQL engine not initialized")
        Base.metadata.create_all(bind=self._postgresql_engine)


# Global database manager instance
db_manager = DatabaseManager()


def get_postgresql_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency for getting a PostgreSQL database session.
    
    Yields:
        Session: A SQLAlchemy database session.
    """
    with db_manager.get_postgresql_session() as session:
        yield session


def get_mongodb_database() -> MongoDatabase:
    """
    FastAPI dependency for getting a MongoDB database instance.
    
    Returns:
        MongoDatabase: The MongoDB database instance.
    """
    return db_manager.get_mongodb_database()

