"""Dataset files."""

import os

data_dir = os.path.dirname(os.path.realpath(__file__))

ATTACK_TEST = os.path.join(data_dir, "attack_test.csv")
ATTACK_TRAIN = os.path.join(data_dir, "attack_train.csv")
BENIGN_TEST = os.path.join(data_dir, "benign_test.csv")
BENIGN_TRAIN = os.path.join(data_dir, "benign_train.csv")

# preprocessing files
PREPROCESSED_TEST = os.path.join(data_dir, "preprocessed_test.csv")
PREPROCESSED_TRAIN = os.path.join(data_dir, "preprocessed_train.csv")
LABELS_TRAIN = os.path.join(data_dir, "labels_train.npy")
LABELS_TEST = os.path.join(data_dir, "labels_test.npy")

# feature extraction files
FEATURES_TEST = os.path.join(data_dir, "features_test.npz")
FEATURES_TRAIN = os.path.join(data_dir, "features_train.npz")

# manually captured data
CAPTURED_DATA = os.path.join(data_dir, "capture.csv")
DEMO_DATA = os.path.join(data_dir, "demo.csv")
