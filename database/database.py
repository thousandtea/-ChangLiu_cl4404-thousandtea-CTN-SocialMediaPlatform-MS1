from sqlalchemy import create_engine
class Database:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)

    def connect(self):
        return self.engine.connect()

    def disconnect(self, connection):
        connection.close()
