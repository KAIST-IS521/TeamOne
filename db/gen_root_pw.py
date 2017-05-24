import utils

if __name__ == "__main__":
    pw = utils.gen_rand_pw(32)
    with open("root.pw", "wt") as f:
        f.write(pw)

