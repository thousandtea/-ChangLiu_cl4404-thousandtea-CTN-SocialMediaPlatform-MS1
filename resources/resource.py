from pydantic import BaseModel
import datetime
from fastapi import HTTPException
from sqlalchemy import text
class User(BaseModel):
    username: str
    email: str
    created_at: datetime.datetime

# Class for insertion only
class Insert(BaseModel):
    username: str
    email: str

# Mock database
# mock_users = {
#     1: User(id=1, username="user1", email="user1@example.com", created_at=datetime.datetime.now()),
#     2: User(id=2, username="user2", email="user2@example.com", created_at=datetime.datetime.now()),
# }
class UsersResource:
    def __init__(self, database):
        self.database = database

    def get_user(self, username: str):
        connection = self.database.connect()
        query = text("SELECT username, email, created_at FROM micro1.users WHERE username = :username")
        result = connection.execute(query, {"username": username}).fetchone()
        self.database.disconnect(connection)

        if result:
            user_data = {
                "username": result[0],
                "email": result[1],
                "created_at": result[2]
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
        query = text("SELECT username, email, created_at FROM micro1.users")
        results = connection.execute(query).fetchall()
        self.database.disconnect(connection)

        users = []
        for result in results:
            user_data = {
                "username": result[0],  # 'username' is the first column
                "email": result[1],  # 'email' is the second column
                "created_at": result[2]  # 'created_at' is the third column
            }
            users.append(User(**user_data))

        return users
    # def create_user(self, user: User):
    #     if user.id in mock_users:
    #         raise HTTPException(status_code=400, detail="User already exists")
    #     mock_users[user.id] = user
    #     return user
    def create_user(self, user_data: Insert):
        connection = self.database.connect()
        transaction = connection.begin()

        # Check if username already exists
        check_query = text("SELECT * FROM micro1.users WHERE username = :username")
        existing_user = connection.execute(check_query, {"username": user_data.username}).fetchone()
        if existing_user:
            transaction.rollback()
            raise HTTPException(status_code=400, detail="User with this username already exists")

        # Add current datetime to 'created_at'
        # user_data.created_at = datetime.datetime.now()

        # Insert new user
        insert_query = text("""
            INSERT INTO micro1.users (username, email) 
            VALUES (:username, :email)
        """)
        connection.execute(insert_query, user_data.dict())
        transaction.commit()

        self.database.disconnect(connection)
        return user_data
    # def update_user(self, user_id: int, user_data: User):
    #     if user_id not in mock_users:
    #         raise HTTPException(status_code=404, detail="User not found")
    #     mock_users[user_id] = user_data
    #     return user_data
    def update_user(self, email: str, new_username: str):
        connection = self.database.connect()
        transaction = connection.begin()

        # Change made: we set email as the primary key so username is the one that changes
        update_query = text("""
            UPDATE micro1.users
            SET username = :new_username
            WHERE email = :email
        """)
        result = connection.execute(update_query, {"new_username": new_username, "email": email})

        # Check if any row was affected
        if result.rowcount == 0:
            transaction.rollback()
            raise HTTPException(status_code=404, detail="User update failed: No user found with the provided email")

        transaction.commit()
        self.database.disconnect(connection)

        return {"message": f"Username {new_username} updated successfully for user with email {email}"}
    # def delete_user(self, user_id: int):
    #     if user_id not in mock_users:
    #         raise HTTPException(status_code=404, detail="User not found")
    #     del mock_users[user_id]
    def delete_user(self, username: str):
        try:
            connection = self.database.connect()
            transaction = connection.begin()

            # Delete user
            delete_query = text("DELETE FROM micro1.users WHERE username = :username")
            result = connection.execute(delete_query, {"username": username})

            # Check if any row was affected
            if result.rowcount == 0:
                transaction.rollback()
                raise HTTPException(status_code=404, detail="User not found")

            transaction.commit()
            self.database.disconnect(connection)
            return {"message": f"User with username {username} deleted"}
        except Exception as e:
            print(f"Error: {e}")
            transaction.rollback()
            raise HTTPException(status_code=500, detail="An error happened")