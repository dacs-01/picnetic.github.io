from src.models import Users, db

class UsersRepository:
    def search_users(self, username):
        found_users = Users.query.filter(Users.user_name.ilike(f'%{username}%')).all()
        print(found_users)
        return found_users

users_repository_singleton = UsersRepository()