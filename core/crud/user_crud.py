from core import logger
from core.database.database import get_engine
from core.models.user_model import User
from core.apis.schemas.requests.user_request import UserCreateRequest
from odmantic import ObjectId  ## for id to string

logging = logger(__name__)


class UserCRUD:
    def __init__(self):
        self.User = User
        self.engine = get_engine()

    async def create(self, user_data: dict):
        try:
            logging.info("Executing UserCRUD.create function")
            user = User(**user_data)
            saved_user = await self.engine.save(user)
            logging.info(f"User created with ID: {saved_user.id}")
            return saved_user
        except Exception as error:
            logging.error(f"Error in UserCRUD.create: {str(error)}")
            raise error

    async def get_by_email(self, email: str):
        try:
            logging.info("Executing UserCRUD.get_by_email function")
            user = await self.engine.find_one(User, User.email == email)
            logging.info(f"User found with email: {email}")
            return user
        except Exception as error:
            logging.error(f"Error in UserCRUD.get_by_email: {str(error)}")
            raise error

    async def get_by_id(self, user_id: str):
        try:
            logging.info("Executing UserCRUD.get_by_id function")
            user = await self.engine.find_one(User, User.id == ObjectId(user_id))
            logging.info(f"User found with ID: {user_id}")
            return user
        except Exception as error:
            logging.error(f"Error in UserCRUD.get_by_id: {str(error)}")
            raise error

    async def update(self, user_id: str, update_data: dict):
        try:
            logging.info("Executing UserCRUD.update function")
            user = await self.get_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )
            for key, value in update_data.items():
                setattr(user, key, value)
            updated_user = await self.engine.save(user)
            logging.info(f"User updated with ID: {user_id}")
            return updated_user
        except Exception as error:
            logging.error(f"Error in UserCRUD.update: {str(error)}")
            raise error

    async def delete(self, user_id: str):
        try:
            logging.info("Executing UserCRUD.delete function")
            user = await self.get_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )
            await self.engine.delete(user)
            logging.info(f"User deleted with ID: {user_id}")
            return {"message": "User deleted successfully"}
        except Exception as error:
            logging.error(f"Error in UserCRUD.delete: {str(error)}")
            raise error

    async def get_all(self):
        try:
            logging.info("Executing UserCRUD.get_all function")
            users = await self.engine.find(User)
            logging.info(f"Found {len(users)} users")
            return users
        except Exception as error:
            logging.error(f"Error in UserCRUD.get_all: {str(error)}")
            raise error
