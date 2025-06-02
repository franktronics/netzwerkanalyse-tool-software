from typing import Tuple

from ..ports import DatabasePort
import sqlite3
from datetime import datetime


class DatabaseAdapter(DatabasePort):
    def __init__(self, db_path: str = "packets.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def insert_analysis(self, nic: str) -> int | None:
        try:
            timestamp = datetime.now().isoformat()

            self.cursor.execute(
                "INSERT INTO analysis (timestamp, nic) VALUES (?, ?)",
                (timestamp, nic)
            )
            analysis_id: int = self.cursor.lastrowid
            self.conn.commit()
            return analysis_id
        except sqlite3.Error as e:
            print(f"Error inserting analysis: {e}")
            self.conn.rollback()
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.conn.rollback()

    def insert_packet(self, src_mac: str, dst_mac: str, raw_data: bytes, analysis_id: str) -> int | None:
        try:
            timestamp = datetime.now().isoformat()

            self.cursor.execute(
                "INSERT INTO packets (timestamp, src_mac, dst_mac, raw_data, analysis_id) VALUES (?, ?, ?, ?, ?)",
                (timestamp, src_mac, dst_mac, raw_data, analysis_id)
            )
            packet_id: int = self.cursor.lastrowid
            self.conn.commit()
            return packet_id
        except sqlite3.Error as e:
            print(f"Error inserting packet: {e}")
            self.conn.rollback()
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.conn.rollback()

    def get_analysis_by_id(self, analysis_id: str) -> Tuple[str, str, str] | None:
        try:
            self.cursor.execute(
                "Select id, timestamp, nic From analysis WHERE id = ?", (analysis_id,)
            )
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching analysis: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def get_packets_by_analysis_id(self, analysis_id: str) -> list[Tuple[str, str, str, str, str, str]] | None:
        self.init_db()
        try: 
            self.cursor.execute(
                """SELECT id, timestamp, src_mac, dst_mac, raw_data, analysis_id
                FROM packets
                WHERE analysis_id=?
                """,
                (analysis_id,)
            )
            rows=self.cursor.fetchall()
            return rows if rows else None
        except sqlite3.Error as e:
            print(f"Error fetching packets: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
        finally:
            self.close_db()

    def get_all_analyses(self) -> list[Tuple[str, str, str]] | None:
        self.init_db()
        try:
            self.cursor.execute("SELECT id, timestamp, nic FROM analysis ORDER BY timestamp DESC")
            return self.cursor.fetchall()
        finally:
            self.close_db()

    def delete_analysis(self, analysis_id) -> bool:      
        try:
            self.init_db()
            self.cursor.execute(
                "DELETE FROM packets WHERE analyse_id = ?", (analysis_id,)
            )
            self.cursor.excecute(
                "DELETE FROM analysis WHERE id =?", (analysis_id,)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error Deleting analysis by ID: {e}")
            self.conn.rollback()
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.conn.rollback()
            return False
        finally:
            self.close_db()

    def init_db(self) -> None:
        try:
            self._connect()
            self._initialize_database()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            raise

    def close_db(self) -> None:
        try:
            if self.conn is None:
                return
            try:
                # Simple test query to check if connection is still open
                self.conn.execute("SELECT 1")

                # Connection is open, so proceed with closing
                if self.cursor is not None:
                    self.cursor.close()
                    self.cursor = None

                self.conn.commit()  # Final commit
                self.conn.close()
                self.conn = None
            except sqlite3.ProgrammingError:
                # Database is already closed -> reset attributes
                self.conn = None
                self.cursor = None
            except sqlite3.Error as e:
                print(f"Error during database connection test: {e}")
                self.conn.close()
                self.conn = None
                self.cursor = None
        except Exception as e:
            print(f"Unexpected error during database closing: {e}")

    def _connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.execute("PRAGMA journal_mode = WAL")
            self.conn.execute("PRAGMA foreign_keys = ON")
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def _initialize_database(self):
        """Initialize database if tables don't exist"""
        try:
            self.cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='analysis'
            """)
            if not self.cursor.fetchone():
                # Create analysis table
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS analysis (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME NOT NULL,
                        nic TEXT NOT NULL
                    )
                ''')

            self.cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='packets'
            """)
            if not self.cursor.fetchone():
                # Create packets table with foreign key reference to analysis
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS packets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        src_mac TEXT NOT NULL,
                        dst_mac TEXT NOT NULL,
                        raw_data BLOB NOT NULL,
                        analysis_id INTEGER,
                        FOREIGN KEY(analysis_id) REFERENCES analysis(id)
                    )
                ''')
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            self.conn.rollback()
            raise

    def __del__(self):
        """Destructor to ensure database connection is closed"""
        self.close_db()
