import pymysql.cursors

class bankDB:
    def __init__(self, host='localhost',
                       user='root',
                       password='DtWb3q2WcG0tc2fFgXi5sGx86XL7RT8g',
                       db='bankDB'):
        '''
            localhost, root, ~
        '''
        self.conn = pymysql.connect(host, user, password, 'bankDB', 
                                    cursorclass=pymysql.cursors.DictCursor)

    
    def match_id_pw(self, user_id, user_pw):
        with self.conn.cursor() as cursor:
            sql = "SELECT * FROM `user_table` WHERE `user_id`=%s \
                   AND `user_pw`=%s"
            cursor.execute(sql, (user_id, user_pw))
            result = cursor.fetchone()
            if result: return True
            else: return False

    def is_existing_id(self, inputted_id):
        with self.conn.cursor() as cursor:
            sql = "SELECT * FROM user_table WHERE user_id = %s"
            cursor.execute(sql, (inputted_id, ))
            result = cursor.fetchone()
            if result: return True
            else: return False

