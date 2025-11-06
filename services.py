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