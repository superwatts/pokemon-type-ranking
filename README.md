# pokemon-type-ranking
A script for ranking every possible Pokemon type combination (262,000+) by their offensive and defensive capabilities.

## The Results
If you aren't interested in running the code on your own, go to the 'outputs' folder on the repository. This contains the records for type combinations of up to 2 types, up to 3 types, and up to 18 types. 

Records ranking combinations up to 'n' types will be named as follows:
- Offense scores: `n_offense_scores.txt`
- Defense scores: `n_defense_scores.txt`
- Full record: `n_types_all.txt`

### How scores are calculated:
Offense scores are determined by how many types can be hit for super effective damage with same-type attack bonus (STAB). For example, a score of 80.00% would indicate that a combo can hit 80.00% of all types for super effective damage.


## How to run
If you want to run the code yourself, do as follows:
1. Install Python if not already on your device. [Download Python here.](https://www.python.org/downloads/)
2. Download `poketypes.zip`. This contains the script poketypes.py and the folder containing type effectiveness charts.
3. Unzip `poketypes.zip` into a new folder.
4. Navigate to the new folder in terminal.
5. OPTIONAL: Set up a virtual environment. This is only if you don't want a Python package floating around your computer. [Guide here.](https://docs.python.org/3/library/venv.html)
6. Install Pandas for Python by executing the following in your terminal: `python -m pip install pandas`. This is how the program reads the type chart.
7. You're ready to start! To run the script itself, execute the following in your terminal: `python poketypes.py <number_types>`, where `<number_types>` is the maximum number of type combinations to calculate, without the <>. For example, to run for 2 types, do: `python poketypes.py 2`. OPTIONAL: Extra arguments can be found under the 'Extra Arguments' section.
9. NOTE: If you are running the scripts for a large number of types (10+), your output files could be very large. The outputs for 18 types, for example, took up a total of almost 300MB. The program will warn you if your output files might be large, as well as provide a size estimate. The program could take a while to run for a large number of types.

## Extra Arguments
There are optional settings for running the program. To enable them, just put the code(s) anywhere after the number of types. For example, `--nofull` could be run for 2 types with `python poketypes.py 2 --nofull`. You can use as many as you would like.
The optional arguments are:
- `--exclusive` - Calculate ONLY type combinations with the input number, and no combinations below. For example, `python poketypes.py 4 --exclusive` would calculate and write ONLY combinations of 4 types - not 3, 2, or 1. Exclusive outputs will be saved in the `outputs/exclusive` folder.
- `--ignore` - Disables the warning dialogue for large numbers of combinations. This could be useful if you're running the script multiple times in a row and don't want to deal with the dialogue each time.
- `--nofull` - Disables writing the full record output, only writing the offense and defense scores. This will save a lot of space, but you won't get all the details for type matchups.
- `--nomulti` - Disables multiprocessing. This will significantly decrease how much of your CPU and RAM the program uses, but will also significantly increase the amount of time it takes to complete large numbers of combinations. For example, calculating for 18 types took about 7 minutes on my laptop with multiprocessing, but it took over 16 minutes without multiprocessing. This is not recommended unless you're babying your CPU and RAM and/or have a lot of time to spare.
- `--nostatus` - Disables printing the progress to the terminal as the program works. This could offer marginal performance improvements, but it might look like your terminal is frozen while the program is running.

## Credits:
All scripting done by me.

NONE OF THIS CODE WAS WRITTEN BY AI.

Type charts made by Mrinal Shankar on Kaggle. [Link here.](https://www.kaggle.com/datasets/mrinalshankar/pokemon-types)
