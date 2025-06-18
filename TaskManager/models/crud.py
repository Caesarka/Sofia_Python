import json


def createBD():
    file = open('tasks.json', 'a')
    file.close()


def readBD():

    try:
        with open('tasks.json', "r") as f:
            data = json.load(f)
    except:
        data = {}
    finally:
        f.close()
    return data


def updateDB_new(task_title, task_description):

    data = readBD()
    data[task_title] = task_description

    with open('tasks.json', 'w') as f:
        json.dump(data, f, indent="")
    f.close()


def updateDB_current():
    pass


def deleteDB_task(task_id):
    data = readBD()
    del data[task_id]

    with open('tasks.json', 'w') as f:
        json.dump(data, f, indent="")
    f.close()

def readDB_task(task_id):
    data = readBD()
    try:
        return data[task_id]
    except:
        print("There is no such task id.")
