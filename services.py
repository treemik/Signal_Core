from datetime import datetime




def add_calendar_item(conn,*,date_begins,date_ends,time_begins,time_ends,title,kind,status,priority):
    cursor=conn.cursor()
    created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if date_begins and not date_ends:
        date_ends=date_begins
    if date_ends < date_begins:
        raise ValueError('date_ends cannot be greater than date_begins')
    if date_begins and not time_begins:
        time_begins=datetime.strptime('00:00','%H:%M')
    if time_begins and not time_ends:
        time_ends=datetime.strptime('23:59','%H:%M')
    date_begins=datetime.strftime(date_begins,'%Y-%m-%d')
    date_ends=datetime.strftime(date_ends,'%Y-%m-%d')
    time_begins=datetime.strftime(time_begins,'%H:%M')
    time_ends=datetime.strftime(time_ends,'%H:%M')


    cursor.execute(
        "INSERT INTO calendar_item (date_begins,date_ends,time_begins,time_ends,title,kind,status,priority,created_at)VALUES(?,?,?,?,?,?,?,?,?)",
        (date_begins,date_ends,time_begins,time_ends,title,kind,status,priority,created_at,)
    )
    item_id = cursor.lastrowid
    return item_id
def list_calendar_items(conn):
    cursor=conn.cursor()
    calendar_list=[]
    cursor.execute(
        "SELECT * FROM calendar_item"
    )
    rows=cursor.fetchall()
    if not rows:
        return {'ok':False,"error":"NO_ITEMS"}
    for calender_id,starts_at,ends_at,title,kind,status,priority,created_at,updated_at in rows:
        calendar_list.append({'id':calender_id,'starts_at':starts_at,'ends_at':ends_at,'title':title,'kind':kind,'status':status,'priority':priority,'created_at':created_at,'updated_at':updated_at})

    return {'ok':True,'data':list(calendar_list)}

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

def update_calendar_item(conn,*,item_id,status,priority):
    cursor=conn.cursor()
    updated_at=datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "SELECT id,status,priority,title FROM calendar_item WHERE id=?",(item_id,)
    )
    row=cursor.fetchone()

    if row is None:
        return {'ok':False,'error':'NO_ITEMS'}
    else:
        original_status=row[1]
        original_priority=row[2]
        title=row[3]
    if status is not None:
        cursor.execute(
            "UPDATE calendar_item SET status=?,updated_at=? WHERE id=?",(status,updated_at,item_id,)
        )
    if priority is not None:
        cursor.execute(
            "UPDATE calendar_item SET priority=?,updated_at=? WHERE id=?",(priority,updated_at,item_id,)
        )
    return{'ok':True,'item_id':item_id,'status':status,'priority':priority,'updated_at':updated_at,'original_status':original_status,'original_priority':original_priority,'title':title}