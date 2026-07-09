class BaseRepository:

    def __init__(self, collection):
        self.collection = collection

    def get_all(self):
        return list(self.collection.find({}, {"_id": 0}))

    def insert_many(self, documents):
        if documents:
            self.collection.insert_many(documents)

    def delete_all(self):
        self.collection.delete_many({})