# pokemon-type-ranking
A script for ranking every possible Pokemon type combination (262,000+) by their offensive and defensive capabilities.

## The Results
If you aren't interested in running the code on your own, go to the 'outputs' folder on the repository. Each record contains scores for all type combinations up to the specified size. For example, the file for 3 types contains type combinations of sizes 1, 2, and 3.

This repo has records for all combinations up to 6 types. The other outputs are too large and GitHub won't let me upload them :(((

If you want to get the results ranking all the combinations, you'll need to run the script yourself for 18 types.

Records ranking combinations up to 'n' types will be named as follows:
- Offense scores: `n_offense_scores.txt`
- Defense scores: `n_defense_scores.txt`
- Full record: `n_types_all.txt`

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

## How scores are calculated:
### Offense Scores:
Offense scores are determined by how many types can be hit for super effective damage with same-type attack bonus (STAB). Every offensive super effective adds `2.0` points to a pre-weighted attack score. Neutral damage adds `1.0`, resistances add `0.5`, and immunities add `0.0`. The pre-weighted score is then divided by the highest possible score `(2.0 * <total_number_of_types>)` to get the percentage of all types hit.

For example:
- `100.0%` --> can hit all other types with super effective STAB.
- `50.0%` --> hits all other types with - at most - normal damage STAB.
- `25.0%` --> can only hit other types with not very effective STAB.
### Defense Scores:
This is a lot more subjective. All defensive matchups are examined, and a score is given for each defensive matchup. My personal rubric I made is as follows:
- `0.0x` adds `2.0`
- `> 0.0x but < 0.5x` adds `1.75`
- `0.5x` adds `1.5`
- `1.0x` adds `1.25`
- `2.0x` adds `0.5`
- `>= 4.0x` adds `0.0`
This score is then divided by the highest possible score `(2.0 * <total_number_of_types>)` to get the percentage.

For example:
- `100.0%` --> immune to all types.
- `75.0%` --> takes 0.5X damage from all types.
- `62.50%` --> takes neutral damage from all other types.
- `25.0%` --> takes 2.0x damage from all other types.

#### My Reasoning:
Of course immunity would add the most. The difference between normally resisting `(0.5x)`, super resisting `(0.25x or lower)`, and being immune `(0.0x)` is small, as I figure once a Pokemon resists a type, any damage becomes negligible the defender isn't excessively fragile. Normal damage `(1.0x)` is the same difference lower because it produced the most satisfying results. I dunno, man. `1.0` would probably also work fine. If you want to change this in your own run, just change the line `NORMAL_DAMAGE = 1.25` under `def setDefenseScore(self)` in the `TypeCombo` class. 

Super effective damage `(2.0x)` is a lot lower than neutral damage, as I figure that's enough to at least two-shot a bulky Pokemon. Ultra effective damage `(>=4.0x)` is much lower than even that, since a 4.0x attack from anything is usually enough to one-shot most Pokemon. There are some defenses even lower than `4.0x`. Over 1,000 combinations have a `32.0x` weakness to some type. For example, `['Normal', 'Ice', 'Rock', 'Dark', 'Steel']` is `32.0x` weak to Fighting. Ouch. I didn't penalize these scores further, since a `4.0x` weakness will have the exact same effect as a `32.0x` weakness - your Pokemon won't survive it either way. 

### Average Scores:
These are just the numerical mean of the offense and defense scores. `(offense_score + defense_score) / 2.0`. Not much else to say.

### Rankings
For each list, type combinations are ranked by their respective scores. When there is a tie, the combination with fewer types is prioritized.

## Future work:
Ranking type offenses and defenses relative to the total number of Pokemon of each type. E.g. Water resistance might be seen as more important than Dragon resistance, since there are more Water types than Dragon types. This wouldn't account for competitive viability, though. There are many more Bug types than Dragon types, for instance, but Bug-type attacks aren't exactly a common threat.

Better output. The long `.txt` file gets the job done, but it would be a lot better in a `.csv` file or something. It could also use better navigation.

Maybe some kind of graphic? Not sure. I'm open to suggestions. 

## Credits:
All scripting done by me.

Type charts made by Mrinal Shankar on Kaggle. [Link here.](https://www.kaggle.com/datasets/mrinalshankar/pokemon-types)

NONE OF THIS CODE WAS WRITTEN BY AI.

