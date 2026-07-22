from pymongo import UpdateOne

from app.core.logger import logger


class BaseRepository:

    def __init__(self, collection):
        self.collection = collection

    def get_all(self, projection=None):
        return list(
            self.collection.find(
                {},
                projection,
            )
        )

    def get_by_key(self, key, value, projection=None):
        return self.collection.find_one(
            {key: value},
            projection,
        )

    def insert_many(self, documents):
        if documents:
            self.collection.insert_many(documents)

    def delete_all(self):
        self.collection.delete_many({})

    def upsert(self, document, key="cve"):
        self.collection.update_one(
            {key: document[key]},
            {"$set": document},
            upsert=True,
        )

    def bulk_upsert(self, documents, key="cve"):
        if not documents:
            return {
                "matched": 0,
                "modified": 0,
                "upserted": 0,
            }

        operations = [
            UpdateOne(
                {key: document[key]},
                {"$set": document},
                upsert=True,
            )
            for document in documents
            if document.get(key)
        ]

        if not operations:
            return {
                "matched": 0,
                "modified": 0,
                "upserted": 0,
            }

        result = self.collection.bulk_write(
            operations,
            ordered=False,
        )

        upserted = len(result.upserted_ids or {})

        logger.info(
            f"[Mongo] bulk_write on '{self.collection.name}' -> "
            f"matched={result.matched_count} "
            f"modified={result.modified_count} "
            f"upserted={upserted}"
        )

        return {
            "matched": result.matched_count,
            "modified": result.modified_count,
            "upserted": upserted,
        }
