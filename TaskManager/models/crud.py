import json


def createBD():
    file = open('tasks.json', 'a')
    file.close()


def readBD():
    with open('tasks.json') as f:
        data = json.load(f)
        print(data)
        return data


def updateDB_new(task_title, task_description):
    try:
        with open('tasks.json', "r") as f:
            data = json.load(f)
    except:
        data = {}
    
    data[task_title] = task_description
    f.close()

    with open('tasks.json', 'w') as f:
        json.dump(data, f, indent="")
    f.close()


def updateDB_current():
    pass


def deleteDB_task(task_id):
    file = open('tasks.json', 'w')
    data = json.load(file)
    data.pop(task_id)
    json.dump(data, file)
    file.close()
