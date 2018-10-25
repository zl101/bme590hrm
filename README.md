# bme590hrm
[![Build Status](https://travis-ci.org/zl101/bme590hrm.svg?branch=master)](https://travis-ci.org/zl101/bme590hrm)
##To Run
+ Use Python 3, install requirements, run python hrm.py
+ Desired stats will be written and stored in json file
+ User will be prompted for configuration information

##Notes
+ For all branches except setup merged on github via pull request
+ For setup branch, forgot to run Travis before merging, ran pytest -v
+ For all other merges, got the green light from travis first
+ If word is encountered in CSV file, program will terminate, not ignore
+ If a given row in csv does not have two elements, program will ignore
+ Output gets less accurate with varying dynamic range for voltages
