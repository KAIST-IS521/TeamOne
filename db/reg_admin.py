import pymysql
import utils
import reg_pubkey

if __name__ == "__main__":
    bank = utils.bankDB()
    rand_pw = utils.gen_rand_pw(19)
    reg_pubkey.register_info("admin")
    bank.store_user('admin', rand_pw,
                    'admin', '', '', 1000)
    del bank
