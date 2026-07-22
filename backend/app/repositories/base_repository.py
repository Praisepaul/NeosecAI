from pymongo import UpdateOne

from app.core.logger import logger


class BaseRepository:

    BULK_BATCH_SIZE = 100

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

        total_matched = 0
        total_modified = 0
        total_upserted = 0

        for start in range(
            0,
            len(operations),
            self.BULK_BATCH_SIZE,
        ):

            batch = operations[start : start + self.BULK_BATCH_SIZE]

            result = self.collection.bulk_write(
                batch,
                ordered=False,
            )

            total_matched += result.matched_count
            total_modified += result.modified_count
            total_upserted += len(result.upserted_ids or {})

            logger.info(
                f"[Mongo] '{self.collection.name}' "
                f"batch "
                f"{min(start + len(batch), len(operations))}/"
                f"{len(operations)}"
            )

        logger.info(
            f"[Mongo] bulk_write complete on "
            f"'{self.collection.name}' -> "
            f"matched={total_matched} "
            f"modified={total_modified} "
            f"upserted={total_upserted}"
        )

        return {
            "matched": total_matched,
            "modified": total_modified,
            "upserted": total_upserted,
        }
