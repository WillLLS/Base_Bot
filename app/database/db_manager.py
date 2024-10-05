import os
import sqlite3
import logging 

from app.database.db_types import user_t, transaction_t, category_t

logger = logging.getLogger(__name__)

def get_db_path():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'database', 'database.db')


class User:
    
    def __init__(self):
        pass
    
    def get(tm_id):
        con = sqlite3.connect(get_db_path())
        cur = con.cursor()
        
        cur.execute("SELECT * FROM user WHERE tm_id = ?", (tm_id,))
        user = cur.fetchone()
        
        if user:
            return user_t(*user)
        else:
            return None
        
    def get_all() -> list[user_t]:
        con = sqlite3.connect(get_db_path())
        cur = con.cursor()
        
        cur.execute("SELECT * FROM user")
        users = cur.fetchall()
        
        users = list(map(lambda x: user_t(*x), users))
        
        return users
    
    def get_other(tm_id) -> user_t:
        con = sqlite3.connect(get_db_path())
        cur = con.cursor()
        
        cur.execute("SELECT * FROM user WHERE tm_id != ?", (tm_id,))
        user = cur.fetchone()
        
        if user:
            return user_t(*user)
        else:
            return None
    
    def get_monthly_balance(tm_id, date):
        from datetime import datetime
        
        date = datetime.now().strftime("%Y/%m")
        
        # Get the transaction from a specific month based on the date
        transactions = Transaction.get_all_month(tm_id, date)
        
        balance = 0
        
        for tx in transactions:
            balance += tx.amount
        
        return balance
        
    def add(tm_id, tm_first_name, tm_username, balance=0):
        con = sqlite3.connect(get_db_path())
        cur = con.cursor()
        
        cur.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (tm_id, tm_first_name, tm_username, balance))
        con.commit()
        
    def update_balance(tm_id, balance):
        con = sqlite3.connect(get_db_path())
        cur = con.cursor()
        
        cur.execute("UPDATE user SET balance = ? WHERE tm_id = ?", (balance, tm_id))
        con.commit()
 