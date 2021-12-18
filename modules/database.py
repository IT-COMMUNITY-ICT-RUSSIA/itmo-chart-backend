import os
import typing as tp

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase
from pydantic import BaseModel, parse_obj_as

from .routers.service.models import (
    AchievementEvent,
    AchievementTemplate,
    Reward,
    RewardEvent,
    Subject,
)
from .routers.user.models import User, UserWithPassword
from .singleton import SingletonMeta


class MongoDbWrapper(metaclass=SingletonMeta):
    """A database wrapper implementation for MongoDB"""

    def __init__(self) -> None:
        """connect to database using credentials"""
        mongo_connection_url: tp.Optional[str] = os.getenv("MONGO_CONNECTION_URL", None)

        if mongo_connection_url is None:
            raise ValueError("MONGO_CONNECTION_URL environment variable not found")

        mongo_client_url: str = str(mongo_connection_url) + "&ssl=true&tlsAllowInvalidCertificates=true"

        if mongo_client_url is None:
            message = "Cannot establish database connection: $MONGO_CONNECTION_URL environment variable is not set."
            raise IOError(message)

        mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(mongo_client_url)

        self._database: AsyncIOMotorDatabase = mongo_client["itmochart"]
        self._users_collection: AsyncIOMotorCollection = self._database["users"]
        self._subjects_collection: AsyncIOMotorCollection = self._database["subjects"]
        self._achievements_collection: AsyncIOMotorCollection = self._database["achievements"]
        self._achievement_events_collection: AsyncIOMotorCollection = self._database["achievement-events"]
        self._rewards_collection: AsyncIOMotorCollection = self._database["rewards"]
        self._reward_events_collection: AsyncIOMotorCollection = self._database["reward_events"]

    @staticmethod
    async def _get_element_by_key(
        collection_: AsyncIOMotorCollection,
        key: str,
        value: str,
        model: tp.Type[BaseModel],
    ) -> BaseModel:
        """retrieves all documents from given collection by given {key: value}"""
        result: tp.Dict[str, tp.Any] = await collection_.find_one({key: value}, {"_id": 0})

        if not result:
            raise KeyError("Entry not found")

        return parse_obj_as(model, result)

    @staticmethod
    async def _count_documents_in_collection(collection_: AsyncIOMotorCollection) -> int:
        """Count documents in given collection"""
        count: int = await collection_.count_documents({})
        return count

    @staticmethod
    async def _add_document_to_collection(collection_: AsyncIOMotorCollection, item_: BaseModel) -> None:
        """Push document to given MongoDB collection"""
        await collection_.insert_one(item_.dict())

    @staticmethod
    async def _remove_document_from_collection(collection_: AsyncIOMotorCollection, key: str, value: str) -> None:
        """Remove document from collection by {key:value}"""
        await collection_.find_one_and_delete({key: value})

    @staticmethod
    async def _update_document_in_collection(
        collection_: AsyncIOMotorCollection,
        key: str,
        value: str,
        new_data: BaseModel,
        exclude: tp.Optional[tp.Set[str]] = None,
    ) -> None:
        await collection_.find_one_and_update({key: value}, {"$set": new_data.dict(exclude=exclude)})

    @staticmethod
    async def _get_all_from_collection(
        collection_: AsyncIOMotorCollection,
        model_: tp.Type[BaseModel],
        criteria: tp.Optional[tp.Dict[str, tp.Any]] = None,
    ) -> tp.List[BaseModel]:
        """retrieves all documents from the specified collection"""
        return tp.cast(
            tp.List[BaseModel],
            [
                parse_obj_as(model_, document)
                for document in await collection_.find(criteria or {}, {"_id": 0}).to_list(length=None)
            ],
        )

    @staticmethod
    async def _insert_document(collection: AsyncIOMotorCollection, model_: BaseModel) -> None:
        """insert document to the provided collection"""
        await collection.insert_one(model_.dict())

    async def add_user(self, user: User) -> None:
        """upload User to database"""
        return await self._insert_document(self._users_collection, user)

    async def get_user_by_isu_id(self, isu_id: str) -> UserWithPassword:
        """get user by its isu number from the DB and return it's model"""
        return await self._get_element_by_key(self._users_collection, "isu_id", isu_id, UserWithPassword)

    async def get_all_users(self) -> tp.List[User]:
        """get all available users"""
        return await self._get_all_from_collection(self._users_collection, User)

    async def get_all_teachers(self) -> tp.List[User]:
        """get only teachers"""
        return await self._get_all_from_collection(self._users_collection, User, {"is_teacher": True})

    async def get_all_students(self) -> tp.List[User]:
        """get only students"""
        return await self._get_all_from_collection(self._users_collection, User, {"is_teacher": False})

    async def get_all_students_by_megafaculty(self, megafaculty: str) -> tp.List[User]:
        """get only students from the specified megafaculty"""
        return await self._get_all_from_collection(
            self._users_collection,
            User,
            {"is_teacher": False, "megafaculty": megafaculty},
        )

    async def get_all_students_by_faculty(self, faculty: str) -> tp.List[User]:
        """get only students from the specified faculty"""
        return await self._get_all_from_collection(
            self._users_collection,
            User,
            {"is_teacher": False, "faculty": faculty},
        )

    async def get_all_students_by_program(self, program: str) -> tp.List[User]:
        """get only students from the specified program"""
        return await self._get_all_from_collection(
            self._users_collection,
            User,
            {"is_teacher": False, "program": program},
        )

    async def get_all_students_by_group(self, group: str) -> tp.List[User]:
        """get only students from the specified group"""
        return await self._get_all_from_collection(
            self._users_collection,
            User,
            {"is_teacher": False, "group": group},
        )

    async def add_achievement(self, achievement: AchievementTemplate) -> None:
        """upload Achievement to database"""
        return await self._insert_document(self._achievements_collection, achievement)

    async def get_all_achievements(self) -> tp.List[AchievementTemplate]:
        """get all available achievement templates"""
        return await self._get_all_from_collection(self._achievements_collection, AchievementTemplate)

    async def add_achievement_event(self, achievement: AchievementEvent) -> None:
        """upload Achievement event to database"""
        return await self._insert_document(self._achievement_events_collection, achievement)

    async def get_all_recieved_achievements_for_user(self, user: User) -> tp.List[AchievementEvent]:
        """get all achievements recieved by the specified user"""
        return await self._get_all_from_collection(
            self._achievement_events_collection, AchievementEvent, {"user_id": user.isu_id}
        )

    async def get_all_created_achievements(self, user: User) -> tp.List[User]:
        """get all the achievements created by the user"""
        return await self._get_all_from_collection(
            self._achievement_events_collection, AchievementEvent, {"creator_id": user.isu_id}
        )

    async def add_subject(self, subject: Subject) -> None:
        """upload subject to database"""
        return await self._insert_document(self._subjects_collection, subject)

    async def get_all_subjects(self) -> tp.List[Subject]:
        """get all available subjects"""
        return await self._get_all_from_collection(self._subjects_collection, Subject)

    async def add_reward(self, reward: Reward) -> None:
        """upload Reward to database"""
        return await self._insert_document(self._rewards_collection, reward)

    async def get_all_rewards(self) -> tp.List[Reward]:
        """get all available rewards"""
        return await self._get_all_from_collection(self._rewards_collection, Reward)

    async def add_reward_event(self, reward_event: RewardEvent) -> None:
        """upload reward-event to database"""
        return await self._insert_document(self._rewards_collection, reward_event)

    async def get_all_reward_events(self) -> tp.List[RewardEvent]:
        """get all available reward assignment events"""
        return await self._get_all_from_collection(self._reward_events_collection, RewardEvent)

    async def get_all_reward_events_for_user(self, user: User) -> tp.List[RewardEvent]:
        """get all available reward assignment events for a user"""
        return await self._get_all_from_collection(
            self._reward_events_collection, RewardEvent, {"user_id": user.isu_id}
        )
