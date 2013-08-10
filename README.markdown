# PyUnzip-UNICODE

This project is forked from [WowPyUnzip](https://github.com/yftzeng/WowPyUnzip). Big thanks for original author - Yi-Feng, Tzeng(ant)


## TODO List

+ default encoding
+ install script for unbuntu
+ make the package independently
+ zip file encoding conversion
+ integrate with nautilus,thunar
+ *auto detect correct encoding method*
+ maybe a simple UI for non-terminal geek


## Usage

1. Normal usage

        python unzip.py file.zip

2. Extract zip file with password

        python unzip.py -p password

3. Default encoding is Traditional Chinese(cp950). For Simplified Chinese(cp936), assign 'cp936' to '-e'

        python unzip.py -e cp936 -p password


## Required

- Python 2.6,2.7


