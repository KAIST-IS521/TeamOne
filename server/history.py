from tabulate import tabulate
from util import *

def user_check_history(conn, user):
    print_logo(conn)
    conn.sendall(b" [ Check Transaction History ]\n" +
                 b" Hello, " + user.encode() + b".\n\n" + COR_RESULT)


    # TODO: SQL request and get history (sorting desc order)
    
    # tmp value for testing
    tmp = [[3, '2017-05-14 16:23:34', 'mom', 0, 2000, 2500],
            [2, '2017-05-14 13:34:34', 'sister', 500, 0, 500],
            [1, '2017-05-13 17:55:55', 'admin', 0, 1000, 1000]]

    # make table to show
    table = tabulate(tmp, headers=['No.', 'Date', 'Sender/Receiver','Withdrawn amount',
                 'Deposited amount', 'Balance'], tablefmt='orgtbl')
    conn.sendall(table.encode())
    
    conn.sendall(COR_BASE +
                 b"\n\n Enter any key to return to the previous menu -> ")

    # get any input from user to return previous menu
    data = recv_line(conn)
