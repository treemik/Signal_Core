import argparse
from helper_functions import init_db, DatabaseContextManager
from services import add_calendar_item, list_calendar_items

parser = argparse.ArgumentParser(description='A cli based lifer tracking system centered around a calendar')
subparsers=parser.add_subparsers(dest='command')
subparsers.require=True

add_parser=subparsers.add_parser("add_calendar_item",help="Add a calendar item to an existing database")
add_parser.add_argument('-t','--title',required=True,help="The title of the item")
add_parser.add_argument('-k','--kind',required=True, choices=['plan','task','event','note','checkpoint'],help="The kind of the item (must be plan, task, event, note, checkpoint)")
add_parser.add_argument('-s','--status',required=True,choices=['planned','done','skipped','canceled'],help='the status of the item(must be planned, done, skipped, canceled)')
add_parser.add_argument('-p','--priority',required=True,type=int,choices=[0,1,2,3],help='the priority of the item (must be 0, 1, 2, 3)')
add_parser.add_argument('-b','--begins',required=True,type=int,help='the beginning of the time range (inclusive)')
add_parser.add_argument('-e','--ends',required=True,type=int,help='the end of the time range (inclusive)')
# need to create a better type for the begins and ends argument one that enforces date and time using a datetime object
add_parser=subparsers.add_parser("list_calendar_items",help="List all calendar items in a database")

args = parser.parse_args()
init_db()

if args.command == 'add_calendar_item':
    with DatabaseContextManager("signal_core.db") as conn:
        add_calendar_item(conn,starts_at=args.begins,ends_at=args.ends,title=args.title,kind=args.kind,status=args.status,priority=args.priority)

if args.command == 'list_calendar_items':
    with DatabaseContextManager("signal_core.db") as conn:
        results= list_calendar_items(conn)
        my_string="--All calendar items--"
        print('-'*77)
        print(f"{my_string:^77}")
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

