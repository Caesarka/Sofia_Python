import sqlite3

import os
print("Database path:", os.path.abspath("to_do_data.db"))


def create_DB_conn():
    conn = sqlite3.connect('to_do_data.db')
    cur = conn.cursor()
    var = cur.execute("SELECT * FROM task;")
    data = var.fetchall()
    print(data)
    cur.close()
    conn.close()


def readBD():
    conn = sqlite3.connect('to_do_data.db', isolation_level=None)
    cur = conn.cursor()
    var = cur.execute("SELECT * FROM task;")
    data = var.fetchall()
    print(data)
    cur.close()
    conn.rollback()
    conn.close()
    return data


def task_create(task_title, task_description):

    conn = sqlite3.connect('to_do_data.db')
    cur = conn.cursor()
    new_task = cur.execute(
        "INSERT INTO task (title, description, status, priority) VALUES (?, ?, ?, ?);", (task_title, task_description, 1, 1))
    conn.commit()
    cur.execute("SELECT * FROM task ORDER BY id DESC LIMIT 1;")
    new_task = cur.fetchone()

    cur.close()
    conn.close()
    return new_task


def task_update(id, task_title, task_description, status, priority):
    conn = sqlite3.connect('to_do_data.db')
    cur = conn.cursor()
    update_task = cur.execute("UPDATE task SET title = ?, description = ?, status = ?, priority = ? WHERE id = ?;",
                              (task_title, task_description, status, priority, id))
    conn.commit()
    cur.execute("SELECT * FROM task WHERE id = ?;", (id,))
    update_task = cur.fetchone()

    cur.close()
    conn.close()
    return update_task


def task_delete(task_id):
    print(task_id)

    conn = sqlite3.connect('to_do_data.db')
    cur = conn.cursor()

    cur.execute("DELETE FROM task WHERE id = ?;", (task_id,))
    res = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    print(res)

    if not res:
        raise ValueError(f"Task with id {task_id} not found")
    return True


def task_read(task):
    print(type(task[0]))
    conn = sqlite3.connect('to_do_data.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM task WHERE id = {task[0]};")
    result = cur.fetchone()
    print(result)
    cur.close()
    conn.close()
    if result:
        return result
    else:
        print("There is no such task id.")
