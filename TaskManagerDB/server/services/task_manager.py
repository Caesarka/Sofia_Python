from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from model.task import Task


class TaskManager:
    def __init__(self, engine):
        self.engine = engine

    def add_task(self, task: Task) -> Task | None:
        """
        Description:
            create new task
        Args:
            task: Task
        Returns:
            The method creates new Task object or returns None if data isn't correct
        """
        with Session(self.engine) as session:
            session.add(task)
            session.flush()

            return task
        
    def add_task_by_fields(self, title: str, description: str, status: str, priority: str) -> Task | None:
        """
        Description:
            create new task
        Args:
            title: Task title
            description: Task description
            status: status
            priority: priority
        Returns:
            The method creates new Task object or returns None if data isn't correct
        """
        with Session(self.engine) as session:
            existing_task = select(Task).where(Task.title == title)

            if session.scalars(existing_task).first():
                raise ValueError(f"Task with title {title} already exists")

            new_task = Task(title=title, description=description,
                            status=status, priority=priority)
            session.add(new_task)
            session.commit()

            print(f"Task {new_task} was created")
            return new_task

    def update_task(self, id: int, title: str, description: str, status: str, priority: str) -> Task | None:
        """
        Description:
            update task
        Args:
            title: Task title
            description: Task description
            status: status
            priority: priority
        Returns:
            The method update existing Task object or returns None if data isn't correct
        """
        with Session(self.engine) as session:
            existing_task = select(Task).where(Task.id == id)

            if session.scalars(existing_task).first():
                print(f"Task with title {title} exists")
                updated_task = update(Task).where(Task.id == id).values(
                    title=title, description=description, status=status, priority=priority)
                session.commit()
                print(f"Task was updated")
                print(updated_task.id)
                return updated_task
            else:
                print(f"There is no task with title {title}")
                return None


if __name__ == "__main__":
    engine = create_engine("sqlite:///to_do_data.db", echo=True)

    #setup_Task_db(engine)

    # 1. Создать экз.класса t_m
    task_manager = TaskManager(engine)

    # 2. Создать через t_m 3 задачи
    task_manager.add_task(
        'New task 1', 'add new test task', 'low', 'In Progress')
    task_manager.add_task('New task 2', 'add new test task', 'medium', 'Done')
    task_manager.add_task('New task 3', 'add new test task', 'high', 'Blocked')

    # 3. Попробовать добавить таску, которая уже есть
    task_manager.add_task(
        'New task 1', 'add new test task', 'low', 'In Progress')


    # 4. попробовать обновить таксу - позитивный исход
    task_manager.update_task(15, 'Updated title for task 1', 'Updated description for task 1')
    # 4. получить 1, несколько и несуществующую таску
#    user_manager.get_user_by_name('Anna')
#    data = user_manager.get_all_users()
#    print(data)
#    user_manager.get_user_by_name('Kate')
#
#    # 5. удалить какую-то таску
#    user_manager.delete_user('Anna')
#    user_manager.delete_user('Nina')
#
#    # 6. попробовать выполнить проверку пароля
#    for elem in data_example:
#        user_manager.check_user_password(elem[0], elem[1])
