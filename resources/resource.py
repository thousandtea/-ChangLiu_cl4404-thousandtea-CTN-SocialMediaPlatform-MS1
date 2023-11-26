from pydantic import BaseModel
import datetime
from fastapi import HTTPException
from sqlalchemy import text
class User(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime.datetime

# Mock database
mock_users = {
    1: User(id=1, username="user1", email="user1@example.com", created_at=datetime.datetime.now()),
    2: User(id=2, username="user2", email="user2@example.com", created_at=datetime.datetime.now()),
}
class UsersResource:
    def __init__(self, database):
        self.database = database

    def get_user(self, user_id: int):
        connection = self.database.connect()
        query = text("SELECT * FROM micro1.users WHERE id = :user_id")
        result = connection.execute(query, {"user_id": user_id}).fetchone()
        self.database.disconnect(connection)

        if result:
            user_data = {
                "id": result[0],
                "username": result[1],
                "email": result[2],
                "created_at": result[3]
            }
            return User(**user_data)

        raise HTTPException(status_code=404, detail="User not found")

    # def get_user_profile(self, user_id: int):
    #     # Mock profile data, replace with real data handling
    #     if user_id in mock_users:
    #         return {"profile": f"Profile of user {user_id}"}
    #     raise HTTPException(status_code=404, detail="User not found")

    # def get_all_users(self):
    #     return list(mock_users.values())
    def get_all_users(self):
        connection = self.database.connect()
        query = text("SELECT id, username, email, created_at FROM micro1.users")
        results = connection.execute(query).fetchall()
        self.database.disconnect(connection)

        users = []
        for result in results:
            user_data = {
                "id": result[0],  # 'id' is the first column
                "username": result[1],  # 'username' is the second column
                "email": result[2],  # 'email' is the third column
                "created_at": result[3]  # 'created_at' is the fourth column
            }
            users.append(User(**user_data))

        return users
    # def create_user(self, user: User):
    #     if user.id in mock_users:
    #         raise HTTPException(status_code=400, detail="User already exists")
    #     mock_users[user.id] = user
    #     return user
    def create_user(self, user: User):
        try:
            connection = self.database.connect()
            # Check if user already exists
            check_query = text("SELECT * FROM micro1.users WHERE id = :id")
            existing_user = connection.execute(check_query, {"id": user.id}).fetchone()

            # Insert new user
            insert_query = text("""
                INSERT INTO micro1.users (id, username, email, created_at) 
                VALUES (:id, :username, :email, :created_at)
            """)
            result = connection.execute(insert_query, user.dict())
            self.database.disconnect(connection)
            print("Inserted user:", result)
            return user
        except Exception as e:
            print(f"An error occurred: {e}")
            raise HTTPException(status_code=500, detail="User already exists")
    # def update_user(self, user_id: int, user_data: User):
    #     if user_id not in mock_users:
    #         raise HTTPException(status_code=404, detail="User not found")
    #     mock_users[user_id] = user_data
    #     return user_data
    def update_user(self, user_id: int, user_data: User):
        connection = self.database.connect()
        # Check if user exists
        check_query = text("SELECT * FROM users WHERE id = :id")
        existing_user = connection.execute(check_query, {"id": user_id}).fetchone()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update user data
        update_query = text("""
            UPDATE users 
            SET username = :username, email = :email, created_at = :created_at
            WHERE id = :id
        """)
        connection.execute(update_query, user_data.dict())
        self.database.disconnect(connection)
        return user_data

    # def delete_user(self, user_id: int):
    #     if user_id not in mock_users:
    #         raise HTTPException(status_code=404, detail="User not found")
    #     del mock_users[user_id]
    def delete_user(self, user_id: int):
        connection = self.database.connect()
        # Check if user exists
        check_query = text("SELECT * FROM users WHERE id = :id")
        existing_user = connection.execute(check_query, {"id": user_id}).fetchone()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete user
        delete_query = text("DELETE FROM users WHERE id = :id")
        connection.execute(delete_query, {"id": user_id})
        self.database.disconnect(connection)
        return {"message": f"User with id {user_id} deleted"}