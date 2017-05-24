import rand_pw

if __name__ == "__main__":
    pw = rand_pw.gen_rand_pw(32)
    with open("root.pw", "wt") as f:
        f.write(pw)

