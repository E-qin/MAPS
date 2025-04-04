import datetime
import logging
import os
import pickle
import random
from typing import Any, Dict, NoReturn, List
import yaml
import numpy as np
import torch
import torch.nn as nn

from utils import const



def pad_and_stack(arrays, pad_value):
    for i, array in enumerate(arrays):
        if array.ndim == 1:
            arrays[i] = array[np.newaxis,:]

    max_cols = max(array.shape[-1] for array in arrays)

    padded_arrays = []
    for array in arrays:
        current_cols = array.shape[-1]
        if current_cols < max_cols:
            padding = np.full((array.shape[0], max_cols - current_cols), pad_value)
            array = np.hstack([array, padding])
        padded_arrays.append(array)

    return np.vstack(padded_arrays)

def format_time(seconds):
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(days)}d {int(hours)}h {int(minutes)}m {seconds:.2f}s"



def setup_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    torch.use_deterministic_algorithms(True)
    os.environ['PYTHONHASHSEED'] = str(seed)  # hash
    os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'


GLOBAL_SEED = 1


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


GLOBAL_WORKER_ID = None


def worker_init_fn(worker_id):
    # set_seed(const.random_seed)
    global GLOBAL_WORKER_ID
    GLOBAL_WORKER_ID = worker_id
    set_seed(GLOBAL_SEED + worker_id)


def load_pickle(path):
    return pickle.load(open(path, 'rb'))


def count_variables(model: nn.Module) -> int:
    total_parameters = 0
    for name, p in model.named_parameters():
        if p.requires_grad:
            num_p = p.numel()
            total_parameters += num_p

    return total_parameters



def batch_to_gpu(batch: dict, device) -> dict:
    for c in batch:
        if isinstance(batch[c], torch.Tensor):
            batch[c] = batch[c].to(device)
        elif isinstance(batch[c], List):
            batch[c] = [[p.to(device) for p in k] if isinstance(
                k, List) else k.to(device) for k in batch[c]]
    return batch


def ndcg_score(y_true, y_score, k=10):
    """Computing ndcg score metric at k.

    Args:
        y_true (np.ndarray): ground-truth labels.
        y_score (np.ndarray): predicted labels.

    Returns:
        np.ndarray: ndcg scores.
    """
    best = dcg_score(y_true, y_true, k)
    actual = dcg_score(y_true, y_score, k)
    return actual / best


def dcg_score(y_true, y_score, k=10):
    """Computing dcg score metric at k.

    Args:
        y_true (np.ndarray): ground-truth labels.
        y_score (np.ndarray): predicted labels.

    Returns:
        np.ndarray: dcg scores.
    """
    k = min(np.shape(y_true)[-1], k)
    order = np.argsort(y_score)[::-1]
    y_true = np.take(y_true, order[:k])
    gains = 2 ** y_true - 1
    discounts = np.log2(np.arange(len(y_true)) + 2)
    return np.sum(gains / discounts)


def hit_score(y_true, y_score, k=10):
    """Computing hit score metric at k.

    Args:
        y_true (np.ndarray): ground-truth labels.
        y_score (np.ndarray): predicted labels.

    Returns:
        np.ndarray: hit score.
    """
    ground_truth = np.where(y_true == 1)[0]
    argsort = np.argsort(y_score)[::-1][:k]
    for idx in argsort:
        if idx in ground_truth:
            return 1
    return 0


def mrr_score(y_true, y_score):
    """Computing mrr score metric.

    Args:
        y_true (np.ndarray): ground-truth labels.
        y_score (np.ndarray): predicted labels.

    Returns:
        np.ndarray: mrr scores.
    """
    order = np.argsort(y_score)[::-1]
    y_true = np.take(y_true, order)
    rr_score = y_true / (np.arange(len(y_true)) + 1)
    return np.sum(rr_score) / np.sum(y_true)


def format_metric(result_dict: Dict[str, Any]) -> str:
    assert type(result_dict) == dict
    format_str = []
    metrics = np.unique([k.split('@')[0] for k in result_dict.keys()])
    topks = np.unique([int(k.split('@')[1]) for k in result_dict.keys()])
    for topk in np.sort(topks):
        for metric in np.sort(metrics):
            name = '{}@{}'.format(metric, topk)
            m = result_dict[name]
            if type(m) is float or type(m) is np.float32 or type(m) is np.float64:
                format_str.append('{}:{:<.4f}'.format(name, m))
            elif type(m) is int or type(m) is np.int32 or type(m) is np.int64:
                format_str.append('{}:{}'.format(name, m))
    return ','.join(format_str)


def check_dir(file_name: str):
    dir_path = os.path.dirname(file_name)
    if not os.path.exists(dir_path):
        logging.info('make dirs:{}'.format(dir_path))
        os.makedirs(dir_path)


def non_increasing(lst: list) -> bool:
    return all(x >= y for x, y in zip(lst, lst[1:]))


def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_hyperparam(args, load_path=''):

    if not load_path: 
        load_path = f"config/{args.model}_{args.data}.yaml" 
    with open(load_path, 'r') as f:
        configs = yaml.load(f, Loader=yaml.FullLoader)

    for key, value in configs.items():
        setattr(args, key, value)
    return args

