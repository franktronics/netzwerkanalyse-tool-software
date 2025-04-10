import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any

class PacketDatabase:
    def __init__(self, db_path: str = "packets.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA journal_mode = WAL")
        self.cursor = self.conn.cursor()

    def initialize_database(self):
        self.cursor.execute("DROP TABLE IF EXISTS packets")
        self.cursor.execute('''
            CREATE TABLE packets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                data_parsed TEXT,
                raw_packet BLOB
            )
        ''')
        self.conn.commit()

    def insert_packet(self, parsed_data: Dict[str, Any], raw_data: bytes):
        json_data = json.dumps(parsed_data)
        timestamp = datetime.now().isoformat()

        self.cursor.execute('''
            INSERT INTO packets (timestamp, data_parsed, raw_packet)
            VALUES (?, ?, ?)
        ''', (timestamp, json_data, raw_data))
        self.conn.commit()

    def get_all_packets(self) -> List[Dict[str, Any]]:
        self.cursor.execute("SELECT data_parsed, raw_packet FROM packets")
        rows = self.cursor.fetchall()
        results = []

        for data_parsed, raw_packet in rows:
            item = {
                "parsed_data": json.loads(data_parsed),
                "raw_data": raw_packet
            }
            results.append(item)

        return results

    def close(self):
        self.conn.close()
