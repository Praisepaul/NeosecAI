from app.assets.asset_seed import assets
from app.assets.asset_repository import asset_repository


class AssetService:

    def seed(self):

        asset_repository.delete_all()

        asset_repository.bulk_insert(assets)

        return len(assets)

asset_service = AssetService()
