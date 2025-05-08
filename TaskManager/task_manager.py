from asyncio import tasks

class Task:
    __id = 0
    def __init__(self, title, description, priority, status):
        Task.__id += 1
        
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.id = Task.__id

class TaskManager:
    def __init__(self, tasks = {}):
        self.tasks = tasks
        
    def add_task(self):
        title = input("Enter title: ")
        description = input("Enter description: ")
        priority = input("Enter priority: ")
        status = input("Enter status: ")
        task = Task(title, description, priority, status)
        self.tasks[task.id] = task

    
    def remove_task(self):
        id = input("Type task id for remove: ")
        del tasks[id]

    def change_status(self, task, status):
        task.status = status
        
    def __prioprity_sort(current_p, tar_p):
        if current_p == tar_p: return True
        else: return False

    def get_tasks_by_priority(self, priority):
        tasks_by_priority = filter(lambda task: self.__prioprity_sort(task.priority, priority), self.tasks)

        # for t in self.tasks:
        #     if t.priority == priority:
        #         tasks_by_priority.append(t)
        
        return tasks_by_priority
    
    def list_all_tasks(self):
        return self.tasks

task_manager = TaskManager()
task_manager.add_task()
task_manager.add_task()
print(task_manager.tasks)

task_manager.remove_task()
print(task_manager.tasks)

task_manager.change_status('study', 'low')
print(f'Status: {task_manager.status}')

task_manager.add_task(task_manager.work)
print(f"Sort by priority: {task_manager.get_tasks_by_priority('low')}")

print(f"List all tasks: {task_manager.list_all_tasks()}")



