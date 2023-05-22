import os

import numpy as np
import pandas as pd

from boosting.args import parse_args
from boosting.data_loader import Dataset, Preprocess
from boosting.utils import set_seeds
from boosting.boosting import boosting_model

import warnings

warnings.filterwarnings("ignore")


def main(args):
    ######################## DATA LOAD
    print("Load Data")
    train = pd.read_csv(args.data_dir + args.file_name, parse_dates=["Timestamp"])
    test = pd.read_csv(args.data_dir + args.test_file_name, parse_dates=["Timestamp"])

    data = Dataset(train, test)
    data = data.split_data()
    print("Succesfully Split Data")

    ######################## SELECT FEATURE

    FEATURE = [
        "userID",
        "assessmentItemID",
        "KnowledgeTag",
        "elapsed",
        "category_high",
        "timeDelta_userAverage",
        "timestep_1",
        "timestep_2",
        "timestep_3",
        "timestep_4",
        "timestep_5",
    ]
    FEATURE_USER = ["user_answer_mean", "user_answer_cnt", "user_time_mean"]
    FEATURE_ITEM = [
        "item_answer_mean",
        "item_answer_cnt",
        "item_time_mean",
        "wrong_users_mean_elapsed",
        "correct_users_mean_elapsed",
    ]
    FEATURE_TAG = ["tag_exposed", "tag_answer_rate"]

    FEATURE_ELO = ["elo_assessment", "elo_test", "elo_tag"]

    FEATURE += FEATURE_USER
    FEATURE += FEATURE_ITEM
    FEATURE += FEATURE_TAG
    FEATURE += FEATURE_ELO

    ######################## DATA PREPROCESSING

    print("Start Preprocessing Data")
    process = Preprocess(args, data)
    data = process.preprocess()
    print("Succesfully Preprocess Data")

    ######################## MODEL INIT

    model = boosting_model(args, FEATURE)

    ######################## TRAIN

    model.training(data, args)

    ######################## INFERENCE

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    model.inference(data)


if __name__ == "__main__":
    args = parse_args()
    os.makedirs(args.model_dir, exist_ok=True)
    main(args)
