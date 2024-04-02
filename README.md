# Bluetooth Attacks Detector

Machine learning model designed to detect Bluetooth DDoS/DoS attacks.

## Prerequisites

- Python 3.12
- Git

## Development Environment Setup

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

<!-- TODO: update dataset download instructions -->

Download the [dataset](https://www.unb.ca/cic/datasets/iomt-dataset-2024.html)
and place the Bluetooth attack/benign dataset in the `data` directory.
Processed data and models will be saved in the `data` and `models` directories.
Logs will be saved to the root of the project. Dataset statistics and model
evaluation results will be saved in the root of the project as well. The
following is the expected directory structure of un-managed files:

```txt
project_root/
├── data/
│   ├── attack_test.csv
│   ├── attack_train.csv
│   ├── benign_test.csv
│   └── benign_train.csv
├── models/
├── dataset_stats.txt
├── dev.log
└── evaluation.txt
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

Admin privileges are required to run the demonstration script to monitor user
input for pausing and controlling communication type. Run the following to run
the demonstration script on Linux/macOS:

```sh
sudo ./main.py --demo [--verbose]
```

On Windows, run the following commands with PowerShell running with
administrator privileges:

```ps1
.\main.py --demo [--verbose]
```
