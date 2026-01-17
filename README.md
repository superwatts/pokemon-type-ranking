# pokemon-type-ranking
A script for ranking every possible Pokemon type combination (262,000+) by their offensive and defensive capabilities.

## The Results
If you aren't interested in running the code on your own, go to the 'outputs' folder. This contains the records ranking type combinations of up to 2 types, up to 3 types, and up to 18 types. 

Records ranking combinations up to 'n' types will be named as follows:
- Offense scores: `n_offense_scores.txt`
- Defense scores: `n_defense_scores.txt`
- Full record: `n_types_all.txt`

## How to run:
If you want to run the code yourself, do as follows:
1. Install Python if not already on your device. [Download Python here.](https://www.python.org/downloads/)
2. Download `poketypes.zip`. This contains the script poketypes.py and the folder containing type effectiveness charts.
3. Unzip `poketypes.zip` into a new folder.
4. Navigate to the new folder in terminal.
5. OPTIONAL: Set up a virtual environment. This is only if you don't want a Python package floating around your computer. [Guide here.](https://docs.python.org/3/library/venv.html)
6. Install Pandas for Python by executing the following in your terminal: `python -m pip install pandas`. This is how the program reads the type chart.
7. You're ready to start! To run the script itself, execute the following in your terminal: `python poketypes.py <number_types>`, where `<number_types>` is the maximum number of type combinations to calculate. For example, to run for 2 types, do: `python poketypes.py 2`. OPTIONAL: Extra arguments can be found [here.](#Extra-Arguments)
8. NOTE: If you are running the scripts for a large number of types (10+), your output files could be very large. The outputs for 18 types, for example, took up a total of almost 300MB. The program will warn you if your output files might be large, as well as provide a size estimate. The program could take a while to run for a large number of types.


## Credits:
All scripting done by me.

NONE OF THIS CODE WAS WRITTEN BY AI.

Type charts made by Mrinal Shankar on Kaggle. [Link here.](https://www.kaggle.com/datasets/mrinalshankar/pokemon-types)
