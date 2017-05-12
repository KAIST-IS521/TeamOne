REGEX_USERNAME = '^[A-Za-z0-9]{,20}$' # TODO: should be changed based on MySQL
#REGEX_PASSWORD = '' # TODO: should be changed based on MySQL
REGEX_AMOUNT = '^[0-9]*$' 
LEN_PASSWORD = 20 # TODO: should be changed based on MySQL

CLEAR_TERMINAL = "\x1b[2J\x1b[H"

COR_LOGO = "\033[1;36;40m"
COR_BASE = "\033[0;33;40m"
COR_ERRMSG = "\033[1;37;41m"
COR_SUCCESS = "\033[0;30;42m"
COR_DEFAULT = "\033[0m"
COR_RESULT = "\033[1;37;45m"

ERRMSG_OPTION = COR_ERRMSG+ " Invalid input.\n" + COR_BASE

#ERRMSG_USER_LEN = (COR_ERRMSG + " Username should be shorter than " +
#                    str(LEN_USERNAME) + ".\n" + COR_BASE)
ERRMSG_USER_NULL = COR_ERRMSG + " Please input the username.\n" + COR_BASE
ERRMSG_USER_INVAL = COR_ERRMSG + " Invalid username.\n" + COR_BASE

ERRMSG_PW_LEN = (COR_ERRMSG + " Password should be shorter than " + 
                    str(LEN_PASSWORD) + ".\n" + COR_BASE)
ERRMSG_PW_NULL = COR_ERRMSG +  " Please input the password.\n" + COR_BASE

ERRMSG_RECV_NULL = COR_ERRMSG + " Please input the receiver.\n" + COR_BASE
ERRMSG_RECV_INVAL = COR_ERRMSG + " Invalid receiver.\n" + COR_BASE

ERRMSG_WON_NULL = COR_ERRMSG + " Please input amount to transfer.\n" + COR_BASE
ERRMSG_WON_INVAL = COR_ERRMSG + " Invalid amount.\n" + COR_BASE
