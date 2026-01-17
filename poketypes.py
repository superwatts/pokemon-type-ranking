# poketypes.py
#
# This is a program to find the best and worst possible type combinations in Pokemon.

from    datetime        import datetime, timedelta
import  math
from    multiprocessing import Pool, cpu_count
import  os
import  pandas as pd
import  sys

CHART             = pd.read_csv("charts\\Pokemon Type Chart.csv")
CHART             = CHART.set_index(CHART.columns[0])
DO_MULTIPROCESS   = True
EXCLUSIVE         = False # If False, do combos of size [1, N]. If True, do combos of size N only.
WRITE_FULL        = True
FULL_RECORD_KB    = 1.0
O_D_RECORD_KB     = 0.2
WARN              = True
WARNING_THRESHOLD = 10000
WRITE_STATUS      = True

global completed
global total
completed = 0
total = 0

exclusive_str = ""
exclusive_path = ""

TYPES = CHART.columns.to_list()

start_time = datetime.now()

# List of all TypeCombo objects.
all_combos = []

class TypeCombo:
  # Class containing data and logic for type combinations.
  def __init__(self, types_list):
    self.types          = types_list
    self.n_types        = len(types_list)
    self.offenses       = dict.fromkeys(TYPES, 0.0)
    self.defenses       = dict.fromkeys(TYPES, 1.0)
    self.offense_score  = -1
    self.defense_score  = -1
    self.average_score  = -1

    self.is_highest_offense = False
    self.is_highest_defense = False
    self.is_highest_average = False

    self.is_lowest_offense = False
    self.is_lowest_defense = False
    self.is_lowest_average = False

  def getModifiedString(self):
    end_o_str = ""
    end_d_str = ""
    end_a_str = ""
    type_end_str = "types." if self.n_types > 1 else "type."
    if self.is_highest_offense:
      end_o_str = f"\t\tHighest offense for {self.n_types} "  + type_end_str
    elif self.is_lowest_offense:
      end_o_str = f"\t\tLowest offense for {self.n_types} "   + type_end_str
    if self.is_highest_defense:
      end_d_str = f"\t\tHighest defense for {self.n_types} "  + type_end_str
    elif self.is_lowest_defense:
      end_d_str = f"\t\tLowest defense for {self.n_types} "   + type_end_str
    if self.is_highest_average:
      end_a_str = f"\t\tHighest average for {self.n_types} "  + type_end_str
    elif self.is_lowest_average:
      end_a_str = f"\t\tLowest average for {self.n_types} "   + type_end_str
    result = f"{self.types}\n"
    result += f"\t# of Types: {self.n_types}\n"
    result += f"\tOffense Score: {round(self.offense_score,2)}%{end_o_str}\n"
    result += f"\tDefense Score: {round(self.defense_score,2)}%{end_d_str}\n"
    result += f"\tOverall:       {round(self.average_score,2)}%{end_a_str}\n"

    result += "WEAKNESSES:\n"
    has_w = False
    for type, value in self.defenses.items():
      if value > 1.0:
        has_w = True
        result += f"\t{type}: {value}x\n"
    if not has_w:
      result += "\tNone.\n"
    
    has_r = False
    result += "RESISTANCES:\n"
    for type, value in self.defenses.items():
      if value < 1.0 and value > 0.0:
        has_r = True
        result += f"\t{type}: {value}x\n"
    if not has_r:
      result += "\tNone.\n"

    has_i = False
    result += "IMMUNITIES:\n"
    for type, value in self.defenses.items():
      if value == 0.0:
        has_i = True
        result += f"\t{type}: {value}x\n"
    if not has_i:
      result += "\tNone.\n"
  
    has_os = False
    result += "OFFENSIVE SUPER:\n"
    for type, value in self.offenses.items():
      if value > 1.0:
        has_os = True
        result += f"\t{type}: {value}x\n"
    if not has_os:
      result += "\tNone.\n"

    has_or = False
    result += "OFFENSIVE RESIST:\n"
    for type, value in self.offenses.items():
      if value < 1.0 and value > 0.0:
        has_or = True
        result += f"\t{type}: {value}x\n"
    if not has_or:
      result += "\tNone.\n"
    
    has_oi = False
    result += "OFFENSIVE IMMUNE:\n"
    for type, value in self.offenses.items():
      if value == 0.0:
        has_oi = True
        result += f"\t{type}: {value}x\n"
    if not has_oi:
      result += "\tNone.\n"
    
    result = result[0:-1] # Remove trailing '\n'
    return result
  
  def __str__(self):
    return self.get_modified_string(False)

  def updateOffense(self):
    for offense in self.types:
      for defense in TYPES:
        val = CHART.loc[offense, defense]
        self.offenses[defense] = max(val,self.offenses[defense])

  def updateDefense(self):
    for defense in self.types:
      for offense in TYPES:
        val = CHART.loc[offense, defense]
        self.defenses[offense] *= val


  def setOffenseScore(self):
    # Calculate the overall offense quality of this type combination.
    max_score = 2.0 * len(TYPES)
    result = 0.0
    for val in self.offenses.values():
      result += val
    self.offense_score = (result / max_score) * 100.0

  def setDefenseScore(self):
    # Calculate the overall defense quality of this type combination.

    IMMUNE        = 2.0
    SUPER_RESIST  = 1.75
    RESIST        = 1.5
    NORMAL_DAMAGE = 1.25
    WEAK          = 0.5
    SUPER_WEAK    = 0.0

    max_score = IMMUNE * len(TYPES) # Immune to everything.
    result = 0.0
    for val in self.defenses.values():
      if val == 0.0:
        result += IMMUNE
      elif val < 0.5:
        result += SUPER_RESIST
      elif val < 1.0:
        result += RESIST
      elif val == 1.0:
        result += NORMAL_DAMAGE
      elif val == 2.0:
        result += WEAK
      elif val >= 4.0:
        result += SUPER_WEAK
    self.defense_score = (result / max_score) * 100.0

  def populate(self):
    # Take a TypeCombo input and populate its offenses and defenses.
    self.updateOffense()
    self.setOffenseScore()
    self.updateDefense()
    self.setDefenseScore()
    self.average_score = (self.offense_score + self.defense_score) / 2.0

# End of TypeCombo class.

def populateCombo(type_combo):
  # Global scope. Avoid.
  # Take a TypeCombo input and populate its offenses and defenses.
  type_combo.populate()
  return type_combo

def initWorker(combos):
  global all_combos


# ---------------------------------------------------- BEGIN MAIN ----------------------------------------------------



if __name__ == "__main__":
  n_types = len(TYPES)
  if len(sys.argv) >= 2:
    if sys.argv[1].isdigit() and int(sys.argv[1]) > 0:
      N_COMBINATIONS = int(sys.argv[1])
    else:
      print(f"ERROR: Unrecognized argument \"{sys.argv[1]}\". First argument must be the max types per combo. (e.g. 2)")
      print("Exiting program.")
      exit()
    if '--ignore' in sys.argv:
      WARN = False
    if '--nofull' in sys.argv:
      WRITE_FULL = False
    if '--nostatus' in sys.argv:
      WRITE_STATUS = False
    if '--nomulti' in sys.argv:
      DO_MULTIPROCESS = False
    if '--exclusive' in sys.argv:
      EXCLUSIVE = True
      exclusive_str = "_exclusive"
      if not os.path.exists('outputs\\exclusive'):
        os.mkdir('outputs\\exclusive')
      exclusive_path = "exclusive\\"
  if N_COMBINATIONS > n_types:
    print(f"ERROR: Can't make combos of {N_COMBINATIONS} types from {n_types} total types!")
    c = input(f"Continue with combos of {n_types}? (y/n) ")
    c = c.lower()
    if c == 'n':
      print("Exiting program.")
      exit()
    elif c != 'y':
      print("Unrecognized response. Exiting program.")
      exit()
    else:
      N_COMBINATIONS = n_types

  
  lower_bound = N_COMBINATIONS - 1 if EXCLUSIVE else 0
  for k in range(lower_bound+1, N_COMBINATIONS+1):
    total += math.comb(n_types, k)
  if WARN and total > WARNING_THRESHOLD:
    print(f"Computing for groups of {N_COMBINATIONS} will produce {total} total combinations.")
    size_estimate = total*O_D_RECORD_KB*2.0 + total*FULL_RECORD_KB if WRITE_FULL else total*O_D_RECORD_KB*2.0
    unit = "KB"
    if size_estimate > 1000.0:
      size_estimate /= 1000.0
      unit = "MB"
    print(f"Output files together could take up to {round(size_estimate,2)} {unit} of space.")
    print("This might take a while.")
    c = input("Continue anyways? (y/n) ")
    c = c.lower()
    if c == 'n':
      print("Exiting program.")
      exit()
    elif c != 'y':
      print("Unrecognized response. Exiting program.")
      exit()

  def buildCombo(combo_list, n_per_combo, start_i, **kwargs):
    as_class = kwargs.get('as_class', True)
    # We already have the most recent type, now we just add all the other types.
    global all_combos
    if len(combo_list) > n_per_combo or start_i > len(TYPES):
      return
    elif len(combo_list) == n_per_combo:
      if as_class:
        all_combos.append(TypeCombo(combo_list))
      else:
        all_combos.append(combo_list)
      if WRITE_STATUS:
        global completed
        completed += 1
        print(f"\rCreated:           {completed} / {total} ", end="")
    else:
      for i in range(start_i, n_types):
        new_list = combo_list[:]
        new_list.append(TYPES[i])
        #if len(new_list) < n_per_combo:
        buildCombo(new_list, n_per_combo, i + 1, as_class=as_class)

  # Generate list.
  for i in range(lower_bound, N_COMBINATIONS):
    # Make all possible combinations of size [(lower_bound + 1), i]
    for j in range(0, n_types):
      combo_list = [TYPES[j]]
      buildCombo(combo_list, i+1, j+1, as_class=True)
  if WRITE_STATUS:
    print()
    completed = 0

  # Calculate all the data for each type combination.
  # This is the most time consuming part.
  if DO_MULTIPROCESS:
    print("Preparing to multiprocess... ", end = "\r")
    input_combos = all_combos.copy()
    all_combos = []
    with Pool(math.floor(cpu_count()/2)) as p:
      for combo in p.imap_unordered(populateCombo, input_combos):
        all_combos.append(combo)
        completed += 1
        print(f"\rPopulated:         {completed} / {total} ", end="")
    
  else:
    for combo in all_combos:  
      combo.populate()
      if WRITE_STATUS:
        completed += 1
        print(f"\rPopulated:       {completed} / {total} ", end="")#"""
  if WRITE_STATUS:
    print()
    completed = 0

  max_len = 0
  for combo in all_combos:
    test_len = len(str(combo.types))
    if test_len > max_len:
      max_len = test_len


  # ---------------------------------------------------- WRITE OUTPUTS ----------------------------------------------------


  if not os.path.exists("outputs"):
    os.mkdir("outputs")

  # Get mins and maxes
  highest_avg = {}
  lowest_avg  = {}
  highest_off = {}
  lowest_off  = {}
  highest_def = {}
  lowest_def  = {}

  completed = 0

  for combo in all_combos:
    n = combo.n_types
    if not n in highest_avg or highest_avg[n] < combo.average_score:
      highest_avg[n] = combo.average_score
    if not n in lowest_avg or lowest_avg[n] > combo.average_score:
      lowest_avg[n] = combo.average_score
    if not n in highest_off or highest_off[n] < combo.offense_score:
      highest_off[n] = combo.offense_score
    if not n in lowest_off or lowest_off[n] > combo.offense_score:
      lowest_off[n] = combo.offense_score
    if not n in highest_def or highest_def[n] < combo.defense_score:
      highest_def[n] = combo.defense_score
    if not n in lowest_def or lowest_def[n] > combo.defense_score:
      lowest_def[n] = combo.defense_score
    if WRITE_STATUS:
      completed += 1
      print(f"\rFinding extremes:  {completed} / {total} ", end="")
  print()

  # Assign mins and maxes
  completed = 0
  for combo in all_combos:
    n = combo.n_types
    if highest_avg[n] == combo.average_score:
      combo.is_highest_average = True
    elif lowest_avg[n] == combo.average_score:
      combo.is_lowest_average = True
    if highest_off[n] == combo.offense_score:
      combo.is_highest_offense = True
    elif lowest_off[n] == combo.offense_score:
      combo.is_lowest_offense = True
    if highest_def[n] == combo.defense_score:
      combo.is_highest_defense = True
    elif lowest_def[n] == combo.defense_score:
      combo.is_lowest_defense = True
    if WRITE_STATUS:
        completed += 1
        print(f"\rLabeling extremes: {completed} / {total} ", end="")
  print()
  if WRITE_FULL:
    completed = 0
    output = open(f"outputs\\{exclusive_path}{N_COMBINATIONS}_types_all{exclusive_str}.txt", 'w')
    print("Sorting by average score... ", end = "")
    all_combos = sorted(all_combos, key = lambda combo: (combo.average_score, abs(n_types - combo.n_types)), reverse=True)
    print("complete.")
    highest_scores = {}
    for i in range(0,len(all_combos)):
      combo = all_combos[i]
      output.write(f"Rank {i+1}:\n")
      output.write(combo.getModifiedString() + '\n\n')
      if WRITE_STATUS:
        completed += 1
        print(f"\rFull written:      {completed} / {total} ", end="")
    output.close()
    if WRITE_STATUS:
      print()
      completed = 0

  offense_output = open(f"outputs\\{exclusive_path}{N_COMBINATIONS}_offense_scores{exclusive_str}.txt", 'w')
  print("Sorting offense... ", end = "")
  all_combos = sorted(all_combos, key = lambda combo: (combo.offense_score, abs(n_types - combo.n_types)), reverse=True)
  print("complete.")
  for i in range(0,len(all_combos)):
    combo = all_combos[i]
    
    combo_n = combo.n_types
    end_str = ""
    if combo.is_highest_offense:
      end_str = f"Highest for {combo_n} "
      if combo_n > 1:
        end_str += "types."
      else:
        end_str += "type."
    elif combo.is_lowest_offense:
      end_str = f"Lowest for {combo_n} "
      if combo_n > 1:
        end_str += "types."
      else:
        end_str += "type."

    spaces = ' ' * ( max_len - len(str(combo.types)) + 1)
    offense_output.write(f"Rank {i+1}: \t{combo.types}{spaces}{round(combo.offense_score,2)}%\t{end_str}\n")
    if WRITE_STATUS:
      completed += 1
      print(f"\rOffense written:   {completed} / {total} ", end="")
  offense_output.close()
  if WRITE_STATUS:
    print()
    completed = 0

  defense_output = open(f"outputs\\{exclusive_path}{N_COMBINATIONS}_defense_scores{exclusive_str}.txt", 'w')
  print("Sorting defense... ", end = "")
  all_combos = sorted(all_combos, key = lambda combo: (combo.defense_score, abs(n_types - combo.n_types)), reverse=True)
  print("complete.")
  for i in range(0,len(all_combos)):
    combo = all_combos[i]
    
    combo_n = combo.n_types
    end_str = ""
    if combo.is_highest_defense:
      end_str = f"Highest for {combo_n} "
      if combo_n > 1:
        end_str += "types."
      else:
        end_str += "type."
    elif combo.is_lowest_defense:
      end_str = f"Lowest for {combo_n} "
      if combo_n > 1:
        end_str += "types."
      else:
        end_str += "type."

    spaces = ' ' * ( max_len - len(str(combo.types)) + 1)
    defense_output.write(f"Rank {i+1}: \t{combo.types}{spaces}{round(combo.defense_score,2)}%\t{end_str}\n")
    if WRITE_STATUS:
      completed += 1
      print(f"\rDefense written:   {completed} / {total} ", end="")
  defense_output.close()
  if WRITE_STATUS:
    print()
    completed = 0

  end_time = datetime.now()
  d_time = end_time - start_time

  print(f"\nProgram complete for combos of {N_COMBINATIONS}.\nTime elapsed: {str(d_time).split('.')[0] + '.' + str(d_time).split('.')[1][:2]}")

