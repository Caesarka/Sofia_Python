from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from model.user.user_models import User


class UserManager:
    def __init__(self, engine):
        self.engine = engine

    def add_user(self, user_name: str, password: str) -> User | None:
        """
        Description

        Args:
            user_name: The user name
            password: password
        Returns:
            The method created new User object or returns None if data isn't correct
        """
        with Session(self.engine) as session:
            # Сделать проверку на то, что у пользователя невалидный логин
            if not user_name or user_name.strip() == "" or not password or password.strip() == "":
                raise ValueError('Bad value, empty string')

            # Сделать проверку на то, что пользователь не существует
            existing_user = select(User).where(User.user_name == user_name)

            if session.scalars(existing_user).first():
                raise ValueError(f"User {user_name} already exists")

            # Если не существует, добавить пользователя
            new_user = User(user_name=user_name, password=password)

            session.add(new_user)
            session.commit()

            # Вернуть объект пользователя при успешном создании
            print(f"User {User.user_name} was added")
            return new_user

    def get_user_by_name(self, user_name: str) -> User | None:
        """
        Description

        Args:
            user_name: The user name
        Returns:
            The method returns User or None if there is not such user_name
        """
        with Session(self.engine) as session:
            user = session.scalars(select(User).where(
                User.user_name == user_name)).first()
            if user:
                print(f"User {User.user_name} exists")
                return user
            else:
                raise Exception(f"There is no user {user_name}")

    def get_all_users(self):
        """
        Description

        Args:

        Returns:
            all Users
        """
        with Session(self.engine) as session:
            data = select(User)
            users = session.scalars(data).all()
            for user in users:
                print(user.user_name)
            return list(users)

    def delete_user(self, user_name: str):
        """
        Description

        Args:
            user_name: The user name

        Returns:
            The method removes User object or returns None if data isn't correct
        """
        with Session(self.engine) as session:
            # Сделать проверку на то, что пользователь существует

            existing_user = select(User).where(User.user_name == user_name)
            user_to_delete = session.scalars(existing_user).first()
            if user_to_delete:
                session.delete(user_to_delete)
                session.commit()
                print(f"User {user_name} was removed")
                return True
            else:
                # Если не существует, добавить пользователя
                raise Exception(f"There is no such user")

    def check_user_password(self, user_name: str, password: str):
        """
        Description

        Args:
            user_name: The user name
            password: password
        Returns:
            The method validates user and password
        """
        user = self.get_user_by_name(user_name)

        if user is not None:
            if user.password == password:
                print(f"User {user.user_name}: password is valid")
            else:
                print(f"User {user.user_name}: password is incorrect")
        else:
            print(f"There is no user {user}")

        return user


data_example = [
    ['Anna', 'efwef'],
    ['Alex', 'adfhahfr'],
    ['Tom', 'adfhahfr']
]

# if __name__ == "__main__":
#
#    engine = create_engine("sqlite:///to_do_data.db", echo=True)
#
#    setup_User_db(engine)
#
#    # 1. Создать экз.класса u_m
#    user_manager = UserManager(engine)
#
#    # 2. Создать через u_m 3х пользователей
#    user_manager.add_user('Anna', 'efwef')
#    user_manager.add_user('Alex', 'adfhahfr')
#    user_manager.add_user('John', 'awerwer')
#
#    # 3. Попробовать добавить пользователя, который уже есть
#    user_manager.add_user('Anna', 'efwef')
#
#    # 4. получить 1, несколько и несуществующего поль-ля
#    user_manager.get_user_by_name('Anna')
#    data = user_manager.get_all_users()
#    print(data)
#    user_manager.get_user_by_name('Kate')
#
#    # 5. удалить какого-то поль-ля
#    user_manager.delete_user('Anna')
#    user_manager.delete_user('Nina')
#
#    # 6. попробовать выполнить проверку пароля
#    for elem in data_example:
#        user_manager.check_user_password(elem[0], elem[1])
#
