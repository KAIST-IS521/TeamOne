import pymysql
import os

# Get the key from ./pubkeys directory - unnecessary func
def get_pgp_key(github_id):
    pubkey_dir = "./pubkeys/"
    pubkey_file = pubkey_dir + github_id + ".pub"
    if not os.path.exists(pubkey_file):
        return None

    pubkey_fp = open(pubkey_file, "r")
    pgp_key = pubkey_fp.read()
    return pgp_key

# Register github_id, pgp_key, reg_flag
def register_info(github_id):
    conn = pymysql.connect(host = 'localhost',
                           user = 'root',
                           password = open("root.pw","rt").read(),
                           db = 'bankDB',
                           charset = 'utf8')
    curs = conn.cursor()

    query = "INSERT INTO auth_table(github_id, reg_flag) \
                    VALUES (%s, %s)"
    try:
        curs.execute(query, (github_id, 0))
        conn.commit()
    except:
        print ("Can't register github_id: %s" % github_id)
        return False
    conn.close()
    return True

if __name__ == "__main__":
    id_list_fp = open("github_id.list", "r")

    while True:
        github_id = id_list_fp.readline()
        if not github_id: break
        github_id = github_id[:-1]
        print (github_id)
        register_info(github_id)

        '''pgp_key = get_pgp_key(github_id)
        if pgp_key is None:
            print ("There is no pubkey file.")
        else:
            register_info(github_id, pgp_key)'''

    id_list_fp.close()
