import time


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

    def upsert(self, document, key="cve"):

        start = time.perf_counter()

        self.collection.update_one(
            {key: document[key]},
            {"$set": document},
            upsert=True
        )

        elapsed = time.perf_counter() - start

        # Only print if the write is unusually slow
        if elapsed > 0.05:
            print(
                f"[MongoDB] Slow upsert ({document.get(key)}): "
                f"{elapsed:.3f} sec"
            )