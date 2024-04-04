import pandas as pd

local_sources = ["localhost ()"]


def rules(packet: pd.DataFrame) -> int:
    threshold = 1000  # check for unusual packet sizes
    threshold_size = 1500  # define the threshold for packet size
    min_size = 20  # define the minimum expected packet size
    threshold_packet_length = 200

    if str(packet["Source"]) in local_sources:
        direction = 0  # incoming
    else:
        direction = 1  # outgoing

    if direction == 0:
        return 1

    if "data" in str(packet["Info"]).lower():
        return 1

    if int(packet["Length"]) > 20:  # type: ignore
        return 1

    return 0


def create_predictor():
    """Create a rule-based predictor of captured data."""

    return rules
