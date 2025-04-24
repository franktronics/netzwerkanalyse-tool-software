import sqlite3
from datetime import datetime
from typing import Dict, Any

class PacketDatabase:
    def __init__(self, db_path: str = "packets.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()
        self.initialize_database()

    def _connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA journal_mode = WAL")
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def initialize_database(self):
        """Initialize database if tables don't exist"""
        try:
            self.cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='packets'
            """)
            if not self.cursor.fetchone():
                self.cursor.execute('''
                    CREATE TABLE packets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        src_mac TEXT NOT NULL,
                        dst_mac TEXT NOT NULL,
                        raw_packet BLOB NOT NULL,
                    )
                ''')
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            raise

    def insert_packet(self, parsed_data: Dict[str, Any], raw_data: bytes):
        """Insert packet data into database"""
        try:
            timestamp = datetime.now().isoformat()
            src_mac = parsed_data["mac"]["src"]
            dst_mac = parsed_data["mac"]["dst"]

            self.cursor.execute('''
                INSERT INTO packets (timestamp, src_mac, dst_mac, raw_packet)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, src_mac, dst_mac, raw_data))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting packet: {e}")
            self.conn.rollback()
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.conn.rollback()

    def close(self):
        """Safely close database connection"""
        try:
            if self.conn:
                self.conn.commit()  # Final commit
                self.cursor.close()
                self.conn.close()
        except sqlite3.Error as e:
            print(f"Error closing database: {e}")
