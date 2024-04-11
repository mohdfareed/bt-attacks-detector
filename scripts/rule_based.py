import pandas as pd  # type: ignore

local_sources = ["localhost ()"]


def rules(packet: pd.DataFrame) -> int:
    # threshold = 1000  # check for unusual packet sizes
    # threshold_size = 1500  # define the threshold for packet size
    # min_size = 20  # define the minimum expected packet size
    # threshold_packet_length = 200

    if "0x000d" in str(packet["Info"]) or "Unknown" in packet["Info"]:
        return 1  # incoming

    if "Offset: 0" in str(packet["Info"]):
        return 1

    if "0x0013" in str(packet["Info"]):
        return 1

    if "data" in str(packet["Info"]).lower():
        return 1

    if int(packet["Length"].iloc[0]) > 20:  # type: ignore
        return 1

    return 0


def create_predictor():
    """Create a rule-based predictor of captured data."""

    return rules
