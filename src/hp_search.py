import green_tsetlin as gt
from green_tsetlin.hpsearch import HyperparameterSearch

from time import perf_counter
import random
import pickle
import os 
import uuid

import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
import tqdm

import green_tsetlin as gt

def get_dataset(data_dir):
    t0 = perf_counter()
    
    dataset_train = pickle.load(open(os.path.join(data_dir, "train_dataset.pkl"),"rb"))
    dataset_test = pickle.load(open(os.path.join(data_dir, "val_dataset.pkl"), "rb"))

    X_train = np.array(dataset_train["images"])
    y_train = np.array(dataset_train["labels"])

    X_test = np.array(dataset_test["images"])
    y_test = np.array(dataset_test["labels"])
    
    X_train = np.where(X_train.reshape((X_train.shape[0], 45 * 45)) > 200, 1, 0)
    X_train = X_train.astype(np.uint8)
        
    X_test = np.where(X_test.reshape((X_test.shape[0], 45 * 45)) > 200, 1, 0)
    X_test = X_test.astype(np.uint8)
    
    y_train = y_train.astype(np.uint32)
    y_test = y_test.astype(np.uint32)

    print("X_train.shape:{}".format(X_train.shape))
    print("y_train.shape:{}".format(y_train.shape))
    print("X_test.shape:{}".format(X_test.shape))
    print("y_test.shape:{}".format(y_test.shape))

    t1 = perf_counter()    
    delta = t1 - t0
    print("getting data time:{}".format(delta))

    return X_train, X_test, y_train, y_test

if __name__=='__main__':
    data_dir = "/home/steffenm/data/cv/dataset"
    xt, xe, yt, ye = get_dataset(data_dir)
    
    hpsearch = HyperparameterSearch(s_space=(2.0, 20.0),
                                clause_space=(1000, 10000),
                                threshold_space=(500, 10000),
                                max_epoch_per_trial=10,
                                literal_budget=(5, 50),
                                k_folds=2,
                                n_jobs=128,
                                seed=42,
                                minimize_literal_budget=False)

    hpsearch.set_train_data(xt, yt)
    hpsearch.set_eval_data(xe, ye)
    
    hpsearch.optimize(n_trials=30, study_name="handwritten math hpsearch", show_progress_bar=True, storage=None)

    params = hpsearch.best_trials[0].params
    performance = hpsearch.best_trials[0].values
    
    print("best paramaters: ", params)
    print("best score: ", performance)

    pickle.dump(params, open("params.pkl", "wb"))
    pickle.dump(performance, open("performance.pkl", "wb"))







