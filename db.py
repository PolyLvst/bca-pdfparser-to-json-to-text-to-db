from sqlalchemy import create_engine, text
from config import Configurer

class DatabaseInserter:
    def __init__(self):
        self.config = Configurer()
        self.DATABASE_URL = self.config.get_db_string()
        self.engine = create_engine(self.DATABASE_URL)
        self.bulk_insert = []
        self.table_name = self.config.get_db_table()

    def append(self, dict_transaction):
        self.bulk_insert.append(dict_transaction)

    def insert(self):
        with self.engine.connect() as conn:
            insert_query = text(f"""
                INSERT INTO {self.table_name} (
                    acno, date, payee, amount, balance, cbg, type, src) 
                VALUES (
                    :acno, :date, :payee, :amount, :balance, :cbg, :type, :source
                )
            """)
            conn.execute(insert_query, self.bulk_insert)
            conn.commit()

    def get_engine(self):
        return self.engine