import btree
import utility

class Database:
    def __init__(self):
        self._db_file = "mydb.db"
        self.dict = {}

        self.stream_of_database = None
        self.database = None

        self.load()
    
    def load(self):
        self.db_open()
        for key in self.database.keys():
            value = utility.decode(self.database[key])
            key = utility.decode(key)
            self.dict.update({key: value})
        self.db_close()
    
    def get(self, key:str, default_value:str=""):
        if key in self.dict.keys():
            return self.dict[key]
        else:
            #self.set(key, default_value)
            return default_value

    def set(self, key:str, value:str):
        self.dict[key] = value
    
    def exists(self, key:str):
        if key in self.dict.keys():
            return True
        else:
            return False
    
    def commit(self):
        self.db_open()
        for key in self.dict.keys():
            value = self.dict[key]
            self.db_set(key, value)
        self.db_commit()
        self.db_close()
    
    def reset(self):
        self.dict = {}
        self.db_reset()
        self.load()

    def db_open(self):
        try:
            self.stream_of_database = open(self._db_file, "r+b")
        except OSError:
            self.stream_of_database = open(self._db_file, "w+b")
        self.database = btree.open(self.stream_of_database)

    def db_set(self, key: str, value: str):
        self.database[utility.encode(key)] = utility.encode(value)

    def db_commit(self):
        self.database.flush()

    def db_close(self):
        self.stream_of_database.close()
        self.database.close()
    
    def db_reset(self):
        utility.remove_a_file(self._db_file)


if "database" not in dir():
    database = Database()