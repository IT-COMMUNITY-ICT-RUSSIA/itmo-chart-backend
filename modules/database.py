import os
import typing as tp

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorCursor
from pydantic import BaseModel

from .models import Employee, Passport, ProductionSchema, ProductionStage, UserWithPassword, NewUser
from .singleton import SingletonMeta


class MongoDbWrapper(metaclass=SingletonMeta):
    """A database wrapper implementation for MongoDB"""

    def __init__(self) -> None:
        """connect to database using credentials"""
        mongo_client_url: str = (
            str(os.getenv("MONGO_CONNECTION_URL")) + "&ssl=true&tlsAllowInvalidCertificates=true"
        )

        print(mongo_client_url)

        if mongo_client_url is None:
            message = "Cannot establish database connection: $MONGO_CONNECTION_URL environment variable is not set."
            raise IOError(message)

        mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(mongo_client_url)

        self._database = mongo_client["itmochart"]

    @staticmethod
    async def _remove_ids(cursor: AsyncIOMotorCursor) -> tp.List[tp.Dict[str, tp.Any]]:
        """remove all MongoDB specific IDs from the resulting documents"""
        result: tp.List[tp.Dict[str, tp.Any]] = []
        for doc in await cursor.to_list(length=100):
            del doc["_id"]
            result.append(doc)
        return result

    async def _get_all_from_collection(
        self, collection_: AsyncIOMotorCollection, model_: tp.Type[BaseModel]
    ) -> tp.List[BaseModel]:
        """retrieves all documents from the specified collection"""
        return tp.cast(
            tp.List[BaseModel],
            [model_(**_) for _ in await collection_.find({}, {"_id": 0}).to_list(length=None)],
        )

    async def _get_element_by_key(
        self, collection_: AsyncIOMotorCollection, key: str, value: str
    ) -> tp.Dict[str, tp.Any]:
        """retrieves all documents from given collection by given {key: value}"""
        result: tp.Dict[str, tp.Any] = await collection_.find_one({key: value}, {"_id": 0})
        return result

    async def _count_documents_in_collection(self, collection_: AsyncIOMotorCollection) -> int:
        """Count documents in given collection"""
        count: int = await collection_.count_documents({})
        return count

    async def _add_document_to_collection(
        self, collection_: AsyncIOMotorCollection, item_: BaseModel
    ) -> None:
        """Push document to given MongoDB collection"""
        await collection_.insert_one(item_.dict())

    async def _remove_document_from_collection(
        self, collection_: AsyncIOMotorCollection, key: str, value: str
    ) -> None:
        """Remove document from collection by {key:value}"""
        await collection_.find_one_and_delete({key: value})

    async def _update_document_in_collection(
        self,
        collection_: AsyncIOMotorCollection,
        key: str,
        value: str,
        new_data: BaseModel,
        exclude: tp.Optional[tp.Set[str]] = None,
    ) -> None:
        if exclude:
            await collection_.find_one_and_update(
                {key: value}, {"$set": new_data.dict(exclude=exclude)}
            )
        else:
            await collection_.find_one_and_update({key: value}, {"$set": new_data.dict()})
