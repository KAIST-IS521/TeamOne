def gen_rand_pw(N):
    import os
    import random
    import string
    random.seed(os.urandom(64))
    return ''.join(random.choice(string.ascii_uppercase + \
                   string.ascii_lowercase + string.digits) \
                   for _ in range(N))
