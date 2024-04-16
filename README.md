# Bluetooth Attacks Detector

Machine learning model designed to detect Bluetooth DoS attacks.

## Prerequisites

- Python 3.12
- Git

## Environment Setup

For Linux or macOS, run the following:

```sh
git clone https://github.com/mohdfareed/bt-attacks-detector.git
cd bt-attacks-detector
./setup.sh
```

For Windows, run the following with PowerShell as an administrator:

```ps1
git clone https://github.com/mohdfareed/bt-attacks-detector.git
Set-Location -Path .\bt-attacks-detector
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\setup.ps1
```

## Usage

Download the [dataset](https://www.unb.ca/cic/datasets/iomt-dataset-2024.html)
and place the Bluetooth attack/benign dataset in the `data` directory.
Processed data and models will be saved in the `data` and `models` directories.
Logs will be saved to the root of the project. Dataset statistics and model
evaluation results will be saved in the root of the project as well. The
following is the expected directory structure of un-managed files:

The dataset above contain mostly attack data, with a relatively small amount of
benign data. Benign data was captured on macOS to balance the dataset using
[PacketLogger](https://www.bluetooth.com/blog/a-new-way-to-debug-iosbluetooth-applications/),
then it was exported to `.btsnoop` format and converted to `.csv` format using
Wireshark. The captured data is not included in the repository due to its size.
The device had 2 headphones, a mouse, a smartwatch, and a game controller
connected to it. This process was repeated twice, once for balancing the
dataset and once to create the data for the demonstration. The captured data
can be downloaded from
[here](https://www.icloud.com/iclouddrive/031kzui9eqKLht9L8aIDuukIQ#capture),
the the demo data an be downloaded from
[here](https://www.icloud.com/iclouddrive/06ecTy11sGg9X8F0eIFS3i3ug#demo).
The final project structure should be as follows:

```txt
project_root/
├── data/
│   ├── benign_test.csv
│   ├── benign_train.csv
│   ├── capture.csv
│   ├── demo.csv
│   ├── dos_test.csv
│   └── dos_train.csv
├── models/
├── dev.log
```

Run the following command to see the usage information:

```sh
source .venv/bin/activate # Linux/macOS
./main.py --help
```

```ps1
.\.venv\Scripts\Activate.ps1 # Windows
.\main.py --help
```

Open the Jupyter notebooks and select the environment `.venv` as the kernel to
run various experiments that were performed.
