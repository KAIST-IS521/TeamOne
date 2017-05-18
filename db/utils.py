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
                                    cursorclass=pymysql.cursors.DictCursor,
                                    autocommit=True)

    
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

    def get_account_num(self, user_id):
        with self.conn.cursor() as cursor:
            sql = "SELECT `account_num` FROM `user_table` \
                   WHERE `user_id`=%s"
            cursor.execute(sql, (user_id, ))
            result = cursor.fetchone()
            if not result: return False
            return result['account_num']

    def get_user_id(self, account_num):
        with self.conn.cursor() as cursor:
            sql = "SELECT `user_id` FROM `user_table` \
                   WHERE `account_num`=%s"
            cursor.execute(sql, (account_num, ))
            result = cursor.fetchone()
            if not result: return False
            return result['user_id']

    def store_user(self, user_id, user_pw, github_id, 
                   email, mobile, balance):
        with self.conn.cursor() as cursor:
            sql = "INSERT INTO user_table(user_id, user_pw, \
                   github_id, email, mobile, balance) \
                   VALUES(%s, %s, %s, %s, %s, %s)"
            try:
                cursor.execute(sql, (user_id, user_pw, github_id, 
                                     email, mobile, balance))
            except:
                return False

    def get_every_user_info(self, user_id):
        with self.conn.cursor() as cursor:
            sql = "SELECT user_pw, account_num, github_id, email, mobile \
                   FROM user_table WHERE user_id = %s"
            cursor.execute(sql, (user_id, ))
            result = cursor.fetchone()
            if not result:
                return False
            else:
                return result

    def store_user_info_modification(self, user_id, info):
        with self.conn.cursor() as cursor:
            user_pw = info['user_pw']
            account_num = info['account_num']
            github_id = info['github_id']
            email = info['email']
            mobile = info['mobile']

            sql = "UPDATE user_table \
                   SET user_pw = %s, account_num = %s, github_id = %s, \
                       email = %s, mobile = %s \
                   WHERE user_id = %s"
            try:
                cursor.execute(sql, (user_pw, account_num, github_id, 
                                     email, mobile, user_id))
                return True
            except:
                return False

    def remove_user_account(self, user_id):
        with self.conn.cursor() as cursor:
            sql = "SELECT account_num, github_id FROM user_table WHERE user_id = %s"
            cursor.execute(sql, (user_id, ))
            info = cursor.fetchone()
            if not info:
                return False

            account_num = info['account_num']
            github_id = info['github_id']

            sql = "DELETE FROM user_table WHERE user_id = %s"
            try:
                cursor.execute(sql, (user_id, ))
            except:
                return False
            
            sql = "INSERT INTO withdraw_account_table(user_id, account_num, \
                                                      github_id) \
                   VALUES(%s, %s, %s)"
            try:
                cursor.execute(sql, (user_id, account_num, github_id))
                return True
            except:
                return False

    def get_balance(self, user_id):
        with self.conn.cursor() as cursor:
            sql = "SELECT `balance` FROM `user_table` WHERE `user_id`=%s"
            cursor.execute(sql, (user_id, ))
            result = cursor.fetchone()
            if not result: return False # No such user
            return result['balance']
    
    def update_balance(self, account, change):
        '''
        positive change => ADD to banalce
        negative change => SUBTRACT from balance
        '''
        with self.conn.cursor() as cursor:
            sql = "UPDATE `user_table` SET `balance`=`balance` + %s " \
                  "WHERE `user_id`=%s"
            try:
                cursor.execute(sql, (change, account))
            except:
                return False
            return True

    def store_transaction(self, user_id, receiver_id, amount, msg):
        with self.conn.cursor() as cursor:
            if not self.update_balance(user_id, -amount):
                # unable to send due to lack of balance
                return False
            self.update_balance(receiver_id, amount)
            
            sender = self.get_account_num(user_id)
            receiver = self.get_account_num(receiver_id)

            sql = "INSERT INTO `tran_table` " \
                  "(`from_account`, `to_account`, `remit`, `msg`) " \
                  "VALUES(%s, %s, %s, %s)"
            try:
                cursor.execute(sql, (sender, receiver, amount, msg))
                return True
            except:
                return False

    def get_all_transaction(self, user_id):
        with self.conn.cursor() as cursor:
            account_num = self.get_account_num(user_id)
            if not account_num:
                return False
            sql = "SELECT tr_time, from_account, to_account, \
                   remit, msg, from_balance, to_balance FROM tran_table \
                   WHERE from_account = %s OR to_account = %s \
                   ORDER BY tr_time"
            cursor.execute(sql, (account_num, account_num))
            result = cursor.fetchall()
            return result

    def close_conn(self):
        self.conn.close()
