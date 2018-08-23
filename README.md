# Email Blaster

## Purpose
A program to allow the sending of mass emails with customisations and minimal dependencies.

## Instructions
```
usage: blast.py [-h] [-s] [-n] [-f CONFIG]

THIS IS STILL UNDERDEVELOPMENT DO NOT USE VERSION: 0.0.3 To run: python3
blast.py -f <config>

optional arguments:
  -h, --help            show this help message and exit
  -s, --sample          Output sample content. [DOES NOT SEND]
  -n, --nosend          Output sample email. [DOES NOT SEND]
  -f CONFIG, --config CONFIG
                        Specify config file. 
```

## Setup
1. Download the folder or perform a 
    ```
    git clone https://github.com/DISMGryphons/Email-blaster.git
    ```
2. Enter the directory
   ```
    cd ./Email-blaster
   ``` 
3. Run to get the manual
   ```
    python3 blast.py -h
   ```
4. Run to try after changing ./Data/account.ini configuration file
   ```
    python3 blast.py -f <configuration file>
   ```

## Disclaimer
Do not use for illegal purposes

This software is licensed under GNU GENERAL PUBLIC LICENSE. Please check `LICENSE` for more details.
