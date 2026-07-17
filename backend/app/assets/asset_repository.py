from app.core.database import db


class AssetRepository:

    COLLECTION = "assets"

    def get_all(self):
        return list(db[self.COLLECTION].find())

    def get_by_hostname(self, hostname):
        return db[self.COLLECTION].find_one({"hostname": hostname})

    def insert(self, asset):
        db[self.COLLECTION].insert_one(asset)

    def bulk_insert(self, assets):

        if assets:
            db[self.COLLECTION].insert_many(assets)

    def upsert(self, asset):

        db[self.COLLECTION].update_one(
            {"hostname": asset["hostname"]},
            {"$set": asset},
            upsert=True,
        )

    def delete_all(self):

        db[self.COLLECTION].delete_many({})


asset_repository = AssetRepository()
