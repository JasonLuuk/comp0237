# COMP0237 - Automated Software Engineering

## Introduction

The repository contains the code I used to run our experiments in a standardised format as well as the results. I ran PyGGI using `--epoch 20` and `--iter 200` in `--mode` `line` and `tree`. The output results and `.diff` files are then compiled using the script in the `results.py` and `apply_diffs.py` file. 

## Setup Instructions

Follow these steps to set up the project and run the experiment on your machine:

### Step 1
Clone the repository into your local [PyGGI](https://github.com/coinse/pyggi) folder.

### Step 2
#### On Linux/Unix:
Run the project using `bash run.sh [bug_name]` in the `comp0237-cw1-code` folder. For example `bash run.sh wrap` will run the experiment for the `wrap` QuixBugs bug.

#### On Windows:
Run the project using `run.bat [bug_name]` in the `comp0237-cw1-code` folder. For example `run.bat wrap` will run the experiment for the `wrap` QuixBugs bug.

### Step 3
That's it! You should now be able to run the project successfully.

## Results

The results should be in the following files in the bug's subfolder:
* `result.txt` contains summary statistics for the experiment on `tree` mode and `line` mode
* `treeResult.txt` and `lineResult.txt` contain the output result of the respective modes
* `diffs` subfolder contains the `.diffs` of the patches found for the `ith` epochs
* `modified` subfolder contains the modified `.py` files by applying the patches found for the `ith` epochs