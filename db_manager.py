from tinydb import TinyDB
import random
import string
import os

class DatabaseManager:
    def __init__(self):
        self.instance: TinyDB = self.get_instance()

    def get_instance(self):
        already_initialized: bool = os.path.exists('db.json')
        instance = TinyDB('db.json')

        if not already_initialized:
            self.initialize(instance)

        return instance
    
    def initialize(self, instance: TinyDB):
        for _ in range(1, 100):
            instance.insert({'userName': ''.join(random.choices(string.ascii_letters + string.digits, k=8)), 'second': random.randint(0, 59), 'minute': random.randint(0, 59), 'hour': random.randint(0, 23),'day': random.randint(1, 31), 'month': random.randint(1, 12), 'year': random.randint(1900, 2024)})

    def get_all(self):
        return self.instance.all()
    
    def add_user(self, name, timestamp):
        val = timestamp.split("/")
        self.instance.insert({'userName' : name, 'second': int(val[5]), 'minute': int(val[4]), 'hour': int(val[3]) ,'day': int(val[2]), 'month': int(val[1]), 'year': int(val[0]) })
    
    def del_user(self, user_id):
        doc_to_delete = self.instance.get(doc_id=user_id)
        
        if doc_to_delete:
            self.instance.remove(doc_ids=[user_id])
