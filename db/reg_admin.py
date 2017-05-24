import pymysql
import utils
import random
import string
import os
import reg_pubkey

def gen_rand_pw(N):
    random.seed(os.urandom(64))
    return ''.join(random.choice(string.ascii_uppercase + \
                   string.ascii_lowercase + string.digits) \
                   for _ in range(N))

if __name__ == "__main__":
    bank = utils.bankDB()
    rand_pw = gen_rand_pw(19)
    reg_pubkey.register_info("admin")
    bank.store_user('admin', rand_pw,
                    'admin', '', '', 1000)
    del bank
