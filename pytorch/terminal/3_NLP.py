import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from torchtext.data import get_tokenizer
from torchtext.datasets import AG_NEWS  # 添加导入

# 情感分析的引用场景
# 产品评论分析
# 社交媒体舆情监控
# 客户服务反馈分类
# 市场趋势预测

# 定义字段处理
TEXT = get_tokenizer('spacy', language='en_core_web_sm')
LABEL = lambda x: int(x)  # 对于数值标签，直接转换为整数

# 加载数据集
train_data, test_data = AG_NEWS(split=('train', 'test'))


# 构建词汇表
TEXT.build_vocab(train_data,
                max_size=25000,
                vectors="glove.6B.100d")