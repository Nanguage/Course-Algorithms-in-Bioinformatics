import os
from os.path import join

DATA_DIR = "./test_data"
FA_FILES = [i for i in os.listdir(DATA_DIR) if i.endswith(".fa")]

RES_PATH = "alg_results"
ALGs = ["nussinov", "maxstacks", "minstackenergy"]

if not os.path.exists(RES_PATH):
    os.mkdir(RES_PATH)

for alg in ALGs:
    for fa in FA_FILES:
        fa_path = join(DATA_DIR, fa)
        res_path = join(RES_PATH, fa.replace(".fa", "")+"."+alg+".structure")
        cmd = "python main.py {} --method {} > {}".format(fa_path, alg, res_path)
        print(cmd)
        os.system(cmd)
