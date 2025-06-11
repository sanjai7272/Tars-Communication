import torch
import torch.nn as nn
import torch.optim as optim
from torchtext.datasets import IMDB
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import Glove
from torchtext import data,datasets
import random

SEED=1234
torch.manual_seed(SEED)
torch.backeds.cudnn.deterministic = True
random.seed(SEED)