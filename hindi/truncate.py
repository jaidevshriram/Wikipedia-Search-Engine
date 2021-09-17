import os
from tqdm.auto import tqdm as tq
from utils import encode32, decode32

src_path = './index-/'
dst_path = '../index-final-truncated/'
os.makedirs(dst_path)
THRESH = 250000

