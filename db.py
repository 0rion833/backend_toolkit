import sqlite3 
from .core import AppError 
 
class SQLiteDB: 
    """Магический менеджер БД.""" 
    def __init__(self, path="app.db"): self.path = path 
    def __enter__(self): 
        self.conn = sqlite3.connect(self.path) 
        self.conn.row_factory = sqlite3.Row 
        return self 
    def __exit__(self, exc_type, exc_val, exc_tb): 
        if exc_type: self.conn.rollback() 
        else: self.conn.commit() 
        self.conn.close() 
    def execute(self, sql, params=()): 
        return self.conn.execute(sql, params) 
    def fetchall(self, sql, params=()): 
        return [dict(r) for r in self.conn.execute(sql, params).fetchall()] 
