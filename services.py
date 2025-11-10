from datetime import datetime




def add_calendar_item(conn,*,starts_at,ends_at,title,kind,status,priority):
    cursor=conn.cursor()
    created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO calendar_item (starts_at,ends_at,title,kind,status,priority,created_at)VALUES(?,?,?,?,?,?,?)",
        (starts_at,ends_at,title,kind,status,priority,created_at,)
    )
def list_calendar_items(conn):
    cursor=conn.cursor()
    calendar_list=[]
    cursor.execute(
        "SELECT * FROM calendar_item"
    )
    rows=cursor.fetchall()
    for calender_id,starts_at,ends_at,title,kind,status,priority,created_at,updated_at in rows:
        calendar_list.append({'id':calender_id,'starts_at':starts_at,'ends_at':ends_at,'title':title,'kind':kind,'status':status,'priority':priority,'created_at':created_at,'updated_at':updated_at})

    return list(calendar_list)

def add_task(conn,*,title,note,due,priority):
    cursor=conn.cursor()
    status='open'
    created_at=datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "INSERT INTO task (title,notes,status,due_at,priority,created_at)VALUES(?,?,?,?,?,?)",
        (title,note,status,due,priority,created_at)
    )
    row=cursor.lastrowid
    return {'task_id':row,'title':title}

def update_task(conn,*,task_id,status,priority):
    cursor=conn.cursor()
    updated_at=datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "SELECT id,status,priority,title FROM task WHERE id=? ",(task_id,)
    )
    row=cursor.fetchone()
    if row is None:
        return {'ok':False,'error':'NO_TASK'}
    else:

        original_status=row[1]
        original_priority=row[2]
        title=row[3]

    if status is not None:
        cursor.execute(
            "UPDATE task SET status=?,updated_at=? WHERE id=?",
            (status,updated_at,task_id,)
        )
    if priority is not None:
        cursor.execute(
            "UPDATE task SET priority=?,updated_at=? WHERE id=?",
            (priority,updated_at,task_id,)
        )
    return {'ok':True,'task_id':task_id,'status':status,'priority':priority,'updated_at':updated_at,'original_status':original_status,'original_priority':original_priority,'title':title}

