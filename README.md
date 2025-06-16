# evaluations

python=3.10 OK

`pip install summ_eval`

**Inputs**:
1. A folder of generated texts: /results   
2. The gold reference file: sorted_charts_output_pew_test.txt

An example generated text file: /results/deepseek-vl2_pew_scatter.txt   
Structure: /results/[model]_[dataset] _[chartType].txt

**Output**:
1. [model]_[chartType].txt

An example output: deepseek-vl2_scatter.txt

#
#

# ROUGE Installation and Setup

# pyrouge - Linux/MacOS

## Pre-requirement

Download https://github.com/bheinzerling/pyrouge

`git clone https://github.com/bheinzerling/pyrouge.git`

Download https://github.com/andersjo/pyrouge/tree/master/tools/ROUGE-1.5.5

`git clone https://github.com/andersjo/pyrouge.git`

`cd pyrouge/tools/ROUGE-1.5.5`

Place the [*andersjo*]pyrouge/ROUGE-1.5.5 -> ..[*bheinzerling*]pyrouge/ROUGE-1.5.5

##

## Build environment commands

python=3.10 OK

`pip install -U  git+https://github.com/bheinzerling/pyrouge.git`

pip uninstall pyrouge

cd pyrouge

pip install -e .

cd ROUGE-1.5.5

pwd

pyrouge_set_rouge_path \`pwd\`

(e.g., pyrouge_set_rouge_path /Users/xxxx/desktop/pyrouge/ROUGE-1.5.5)

chmod +x ROUGE-1.5.5.pl

cd ..

python pyrouge/tests/Rouge155_test.py

#
#

# pyrouge - Windows

`git clone https://github.com/bheinzerling/pyrouge`    
`cd pyrouge`    
`pip install -e .`    

`git clone https://github.com/andersjo/pyrouge.git rouge`    

`cd rouge/tools/ROUGE-1.5.5/`    
`pwd`    

`cd bin`    
`python pyrouge_set_rouge_path /home/pyrouge/rouge/tools/ROUGE-1.5.5/`    

For example: `python pyrouge_set_rouge_path C:/Users/xxx/Downloads/pyrouge/rouge/tools/ROUGE-1.5.5/`    

If you don't have perl.exe, you need to install it (because pyrouge is just a wrapper around the original ROUGE script, which is written in Perl)

You can install http://strawberryperl.com

#
#

## Error Set

### UnicodeDecodeError: 'utf-8' codec can't decode byte 0x80 in position 3131: invalid start byte

`ls -a .DS_Store`

`rm .DS_Store`

###

### UnicodeDecodeError: 'utf-8' codec can't decode byte 0xcf in position 33: invalid continuation byte

Remove all irrelevant files except for decoded and reference .txt files.

### 

### Cannot open exception db file for reading: /pyrouge/pyrouge/ROUGE-1.5.5/data/WordNet-2.0.exc.db

https://github.com/bheinzerling/pyrouge/issues/8

`cd pythonrouge/RELEASE-1.5.5/data/`

`rm WordNet-2.0.exc.db`

`chmod +x WordNet-2.0-Exceptions/buildExeptionDB.pl`

./WordNet-2.0-Exceptions/buildExeptionDB.pl ./WordNet-2.0-Exceptions ./smart_common_words.txt ./WordNet-2.0.exc.db

##

modified (e.g., merged-lines) ROUGE < original ROUGE

##

## REFERENCE

https://medium.com/@prabha88978/installation-working-process-of-rouge-1-5-5-6c0dfdca49e8

https://github.com/bheinzerling/pyrouge/issues/25
