from tabulate import tabulate
from util import *

def user_check_history(conn, user, account_num, obj):
    print_logo(conn)
    conn.sendall(b" [ Check Transaction History ]\n" +
                 b" Hello, " + user.encode() + b" (" +
                 account_num.encode() + b").\n\n" + COR_RESULT)

    # SQL request and get history
    result = obj.get_all_transaction(user)
    
    history = [] # will contain all history

    for idx in reversed(range(len(result))): 
        # if deposited
        if result[idx]['to_account'] == int(account_num):
            party = obj.get_user_id(result[idx]['from_account'])
            history.append([idx+1, result[idx]['tr_time'], 
                str(party) + " (" + str(result[idx]['from_account']) + ")", 0, 
                result[idx]['remit'], result[idx]['to_balance'], 
                result[idx]['msg']])

        # if withdrawn
        else:
            party = obj.get_user_id(result[idx]['to_account'])
            history.append([idx+1, result[idx]['tr_time'], 
                str(party) + " (" + str(result[idx]['to_account']) + ")",
                result[idx]['remit'], 0, result[idx]['from_balance'], 
                result[idx]['msg']])

    # make table to show
    table = tabulate(history, headers=['No.', 'Date', 'Sender/Receiver','Withdrawn amount',
                 'Deposited amount', 'Balance', 'Message'], tablefmt='orgtbl')
    conn.sendall(table.encode())
    
    conn.sendall(COR_BASE +
                 b"\n\n Enter any key to return to the previous menu -> ")

    # get any input from user to return previous menu
    data = recv_line(conn)
