#!/bin/bash -e
# source $PWD/config.sh

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

cd ~
mkdir -p data && cd data
mkdir -p math_expression_data && cd math_expression_data
mkdir -p yolo_data
mkdir -p tm_data

cd ~/data/math_expression_data/yolo_data
gdown https://drive.google.com/uc?id=1ZB12CDhbYZZSqz8Sw1sV00S7-o7Pm4Gb
unzip -q dataset.zip
rm -rf dataset.zip

cd ~/data/math_expression_data/tm_data
gdown https://drive.google.com/uc?id=1unT0LMbMuRDyhfQh5ikHRMpqi5-T9fg2
unzip -q batch_1.zip
rm -rf batch_1.zip