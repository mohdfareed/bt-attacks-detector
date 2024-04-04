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

### Demonstration

The script uses manually captured Bluetooth packets to demonstrate the model's
detection capabilities. The captured data must be at `data/data_capture.csv`.
Data was captured on macOS using
[PacketLogger](https://www.bluetooth.com/blog/a-new-way-to-debug-iosbluetooth-applications/),
then it was exported to `.btsnoop` format and converted to `.csv` format using
Wireshark.

Admin privileges are required to monitor user input for pausing/unpausing
execution. On windows, the script must be run with PowerShell as an
administrator to support this feature. The script can be run in demo mode using
the following commands:

```sh
./main.py --demo [--verbose]      # Linux/macOS - pausing disabled
sudo ./main.py --demo [--verbose] # Linux/macOS - pausing enabled
```

```ps1
.\main.py --demo [--verbose] # Windows
```

## Statistics

### Training Data Summary

```txt
                 No.          Time         Length      Type
count  998391.000000  9.983910e+05  998391.000000  998391.0
mean   499196.000000  4.621494e+05      20.064474       1.0
std    288210.800641  4.679402e+05      12.352341       0.0
min         1.000000  0.000000e+00       4.000000       1.0
25%    249598.500000  2.276077e+03       8.000000       1.0
50%    499196.000000  6.853190e+05      16.000000       1.0
75%    748793.500000  8.540422e+05      32.000000       1.0
max    998391.000000  1.198804e+06     255.000000       1.0
```

### Testing Data Summary

```txt
                 No.           Time         Length      Type
count  251708.000000  251708.000000  251708.000000  251708.0
mean   125854.500000    1071.256077      20.006591       1.0
std     72661.985116     638.578923      12.006976       0.0
min         1.000000       0.000000       5.000000       1.0
25%     62927.750000     601.485238       8.000000       1.0
50%    125854.500000    1050.763037      16.000000       1.0
75%    188781.250000    1669.751179      32.000000       1.0
max    251708.000000    2094.097550      46.000000       1.0
```

### Feature Extraction

- **TF-IDF Vocabulary size:** 609
- **One-Hot Encoding unique categories:** 6
- Standard Scaling mean: 22.7672
- Standard Scaling std: 14.1469
- Feature Hashing features count: 20
- Total number of features: 657

### Model Evaluation

Training accuracy: 0.8341019057652395

#### Confusion Matrix

```txt
[[ 63467   1863]
 [ 50733 200975]]
```

#### Classification Report

```txt
              precision    recall  f1-score   support

           0       0.56      0.97      0.71     65330
           1       0.99      0.80      0.88    251708

    accuracy                           0.83    317038
   macro avg       0.77      0.88      0.80    317038
weighted avg       0.90      0.83      0.85    317038
```
