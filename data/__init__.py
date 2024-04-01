"""Dataset files."""

import os

data_dir = os.path.dirname(os.path.realpath(__file__))

ATTACK_TEST = os.path.join(data_dir, "attack_test.csv")
ATTACK_TRAIN = os.path.join(data_dir, "attack_train.csv")
BENIGN_TEST = os.path.join(data_dir, "benign_test.csv")
BENIGN_TRAIN = os.path.join(data_dir, "benign_train.csv")

# preprocessing files
PREPROCESSED_ATTACK_TEST = os.path.join(data_dir, "processed_attack_test.csv")
PREPROCESSED_ATTACK_TRAIN = os.path.join(
    data_dir, "processed_attack_train.csv"
)
PREPROCESSED_BENIGN_TEST = os.path.join(data_dir, "processed_benign_test.csv")
PREPROCESSED_BENIGN_TRAIN = os.path.join(
    data_dir, "processed_benign_train.csv"
)

# feature extraction files
FEATURES_ATTACK_TEST = os.path.join(data_dir, "features_attack_test.csv")
FEATURES_ATTACK_TRAIN = os.path.join(data_dir, "features_attack_train.csv")
FEATURES_BENIGN_TEST = os.path.join(data_dir, "features_benign_test.csv")
FEATURES_BENIGN_TRAIN = os.path.join(data_dir, "features_benign_train.csv")
