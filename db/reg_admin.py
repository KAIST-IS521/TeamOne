import pymysql
import utils
import rand_pw
import reg_pubkey

if __name__ == "__main__":
    bank = utils.bankDB()
    admin_pw = rand_pw.gen_rand_pw(19)
    reg_pubkey.register_info("admin")
    bank.store_user('admin', admin_pw,
                    'admin', '', '', 1000)
    test1_pw = rand_pw.gen_rand_pw(19)
    bank.store_user('test1', test1_pw,
                    'admin', '', '', 1000)
    test2_pw = rand_pw.gen_rand_pw(19)
    bank.store_user('test2', test2_pw,
                    'admin', '', '', 0)
    with open("test1.pw", "wt") as f:
        f.write(test1_pw)
    with open("test2.pw", "wt") as f:
        f.write(test2_pw)

    del bank
