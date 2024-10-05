from dataclasses import dataclass


@dataclass
class user_t:
    tm_id: str
    tm_first_name: str
    tm_username: str
    balance: int
    
    def __iter__(self):
        return iter([self.tm_id, self.tm_first_name, self.tm_username, self.balance])