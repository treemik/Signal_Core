import argparse
from helper_functions import init_db, DatabaseContextManager, date_type, time_type
from services import add_calendar_item, list_calendar_items, add_task, update_task,update_calendar_item

parser = argparse.ArgumentParser(description='A cli based lifer tracking system centered around a calendar')
subparsers=parser.add_subparsers(dest='command')
subparsers.require=True

add_parser=subparsers.add_parser("add_calendar_item",help="Add a calendar item to an existing database")
add_parser.add_argument('-t','--title',required=True,help="The title of the item")
add_parser.add_argument('-k','--kind',required=True, choices=['plan','task','event','note','checkpoint'],help="The kind of the item (must be plan, task, event, note, checkpoint)")
add_parser.add_argument('-s','--status',required=True,choices=['planned','done','skipped','canceled'],help='the status of the item(must be planned, done, skipped, canceled)')
add_parser.add_argument('-p','--priority',required=True,type=int,choices=[0,1,2,3],help='the priority of the item (must be 0, 1, 2, 3)')
add_parser.add_argument('-b','--date_begins',required=True,type=date_type,help='the beginning of the date range (inclusive)')
add_parser.add_argument('-e','--date_ends',type=date_type,help='the end of the date range (inclusive)')
add_parser.add_argument('-u','--time_begins',type=time_type,help='the beginning of the time range (inclusive)')
add_parser.add_argument('-v','--time_ends',type=time_type,help='the end of the time range (inclusive)')
# need to create a better type for the begins and ends argument one that enforces date and time using a datetime object

add_parser=subparsers.add_parser("list_calendar_items",help="List all calendar items in a database")
# Need to add filters to this so it's not just a search all

add_parser=subparsers.add_parser("update_calendar_item",help="Update a calendar item")
add_parser.add_argument("-i","--id",required=True,type=int,help="The id of the item to update")
add_parser.add_argument("-s","--status",choices=('planned','done','skipped','canceled'),help="The status of the item")
add_parser.add_argument('-p','--priority',choices=[0,1,2,3],type=int,help='the priority of the item (must be 0, 1, 2, 3)')

add_parser=subparsers.add_parser("add_task",help="Add a task")
add_parser.add_argument('-t','--title',required=True,help="The title of the task")
add_parser.add_argument('-n','--note',help = 'The note of the task')
add_parser.add_argument('-d','--due',required=True,type=int,help='The due date of the task')
add_parser.add_argument('-p','--priority',required=True,type=int,choices=[0,1,2,3],help='The priority of the task (must be 0, 1, 2, 3)')

add_parser=subparsers.add_parser("update_task",help="Update a task")
add_parser.add_argument('--id',required=True,help='The id of the task')
add_parser.add_argument('-s','--status', choices=['open','done','blocked'], help='The updated status of the task (must be open, done, blocked)')
add_parser.add_argument('-p','--priority',help='The updated priority of the task')


args = parser.parse_args()
init_db()

if args.command == 'add_calendar_item':
    with DatabaseContextManager("signal_core.db") as conn:
        result=add_calendar_item(conn,date_begins=args.date_begins,date_ends=args.date_ends,time_begins=args.time_begins,time_ends=args.time_ends,title=args.title,kind=args.kind,status=args.status,priority=args.priority)
        text=(f'Calendar item {args.title} added with the ID:{result}')
        text_lenght=len(text)
        print('-'*text_lenght)
        print(text)
        print('-'*text_lenght)

elif args.command == 'list_calendar_items':
    with DatabaseContextManager("signal_core.db") as conn:
        results= list_calendar_items(conn)
        if not results['ok']:
            err=results['error']
            if err=='NO_ITEMS':
                print('No items found')
        else:
            results=results['data']
            print('-'*77)
            print(f"{"--All calendar items--":^77}")
            print('-'*77)
            print(f"{'ID':<4} | {'Title':<10} | {'Kind':<11} | {'Status':<9} | {'Priority':8} | {'Created':<10} | {'Updated'}")
            print("-"*77)
            for result in results:
               calender_id = result['id']
               starts_at = result['starts_at']
               ends_at = result['ends_at']
               title = result['title']
               kind = result['kind']
               status = result['status']
               priority = result['priority']
               created_at = result['created_at']
               updated_at = result['updated_at']
               print (f"{calender_id:<4} | {title[:10]:<10} | {kind:<11} | {status:<9} | {priority:<8} | {created_at[:10]:<10} | {updated_at}")

elif args.command == 'update_calendar_item':
    with DatabaseContextManager("signal_core.db") as conn:
        if not args.status and not args.priority:
            parser.error("You must specify a status or priority or both")
        results=update_calendar_item(conn,item_id=args.id,status=args.status,priority=args.priority)
        if not results['ok']:
            if results['error']=='NO_ITEMS':
                print(f"The task with the id {args.id} does not exist")
        if results['ok']:
            item_id=results['item_id']
            status=results['status']
            priority=results['priority']
            updated_at=results['updated_at']
            original_status=results['original_status']
            original_priority=results['original_priority']
            title=results['title']
            title_length=len(title)
            task_id_length=len(str(item_id))
            string=len("task  with the id  has been updated successfully.")
            string_length=title_length+task_id_length+string

            print('-'*string_length)
            print (f"Task {title} with the id {item_id} has been updated successfully.")
            print('-'*string_length)
            if status is not None:
                print(f"-Status updated from {original_status} to {status}")

            if priority is not None:
                print(f"-Priority updated from {original_priority} to {priority}")

            print (f"-Updated {updated_at}")
            print('-'*string_length)

elif args.command == 'add_task':
    with DatabaseContextManager("signal_core.db") as conn:
        results=add_task(conn,title=args.title,note=args.note,due=args.due,priority=args.priority)
        task_id=results['task_id']
        title=results['title']
        title_length=len(title)
        task_id_length=len(str(task_id))
        string_length=title_length+task_id_length+49
        print('-'*string_length)
        print (f"{'--Adding task successfully--':^{string_length}}")
        print('-'*string_length)
        print(f'The task {title} has been added to the database with id {task_id}')
        print('-'*string_length)


elif args.command == 'update_task':
    with DatabaseContextManager("signal_core.db") as conn:
        if not args.status and not args.priority:
            parser.error("You must specify a status or priority or both")
        results=update_task(conn,task_id=args.id,status=args.status,priority=args.priority)
        if not results['ok']:
            if results['error']=='NO_TASK':
                print(f"The task with the id {args.id} does not exist")
        if results['ok']:
            task_id=results['task_id']
            status=results['status']
            priority=results['priority']
            updated_at=results['updated_at']
            original_status=results['original_status']
            original_priority=results['original_priority']
            title=results['title']
            title_length=len(title)
            task_id_length=len(str(task_id))
            string=len("task  with the id  has been updated successfully.")
            string_length=title_length+task_id_length+string

            print('-'*string_length)
            print (f"Task {title} with the id {task_id} has been updated successfully.")
            print('-'*string_length)
            if status is not None:
                print(f"-Status updated from {original_status} to {status}")

            if priority is not None:
                print(f"-Priority updated from {original_priority} to {priority}")

            print (f"-Updated {updated_at}")
            print('-'*string_length)