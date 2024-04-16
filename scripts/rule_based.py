import logging

import numpy as np
import pandas as pd  # type: ignore

import data

LOGGER = logging.getLogger(__name__)
"""Model training logger."""

last_time = 0.0  # track the last time a packet was received


# 93.2% accuracy on train set (approx 2m processing time)
# 90% accuracy on test set
# 99.8% accuracy on demo data
def rules(packet: pd.DataFrame) -> int:
    global last_time
    time_diff_threshold = 0.00125
    suspicious_lengths = [8, 32]  # suspicious packet lengths

    # calculate time difference between packets
    new_time = float(packet["Time"].iloc[0])
    time_diff = new_time - last_time
    last_time = new_time

    # check for burst traffic and suspicious packet lengths
    is_burst = time_diff < time_diff_threshold
    suspicious_length = int(packet["Length"].iloc[0]) in suspicious_lengths

    if is_burst and suspicious_length:
        return 1
    return 0


# # 45.3% accuracy on train set (approx 10m processing time)
# # 37% accuracy on test set
# # 77.1% accuracy on demo data
# def rules(packet: pd.DataFrame) -> int:
#     # threshold = 1000  # check for unusual packet sizes
#     # threshold_size = 1500  # define the threshold for packet size
#     # min_size = 20  # define the minimum expected packet size
#     # threshold_packet_length = 200

#     if "0x000d" in str(packet["Info"]) or "Unknown" in packet["Info"]:
#         return 1  # incoming

#     if "Offset: 0" in str(packet["Info"]):
#         return 1

#     if "0x0013" in str(packet["Info"]):
#         return 1

#     if "data" in str(packet["Info"]).lower():
#         return 1

#     if int(packet["Length"].iloc[0]) > 20:  # type: ignore
#         return 1

#     return 0


def run():
    LOGGER.info("Testing rule-based prediction...")
    incorrect_predictions = 0  # track incorrect predictions

    LOGGER.debug("Loading dataset...")
    # dataset = pd.read_csv(data.PREPROCESSED_TRAIN)
    # labels = np.load(data.LABELS_TRAIN)
    dataset = pd.read_csv(data.PREPROCESSED_TEST)
    labels = np.load(data.LABELS_TEST)
    # dataset = pd.read_csv(data.DEMO_DATA)
    labels = np.zeros(len(dataset))

    LOGGER.debug("Evaluating...")
    for i, _ in dataset.iterrows():
        row: pd.DataFrame = dataset.iloc[[i]]  # type: ignore
        prediction = rules(row)

        if prediction != labels[i]:  # type: ignore
            incorrect_predictions += 1

    accuracy = 1 - (incorrect_predictions / len(dataset))
    LOGGER.warning(f"Accuracy: {accuracy}")


def create_predictor():
    """Create a rule-based predictor of captured data."""

    return rules
