from typing import Union, List
import random
import re
import math
import unidecode
import logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s-%(levelname)s- %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

basic_mode = [
            ("a", "4"), 
            ("e", "3"),
            ("i", "1"), 
            ("o", "0"),
            ("u", "_")
]



class LeetSpeaker(object):
  def __init__(self, text_in: str, change_prb: float = 0.8, change_frq: float = 0.5, mode: str = "basic", seed: int = None, verbose: bool=False):
    self.text_in = unidecode.unidecode(text_in)
    self.change_prb = change_prb # Probabilidad de que se de un cambio
    self.change_frq = change_frq # Frecuencia del cambio en el texto
    self.mode = mode

    if verbose == True:
      logger.setLevel(logging.INFO)
    else: 
      logger.setLevel(logging.WARNING)    


    random.seed(seed) if seed  else random.seed() # None for full random process, set seed for reproducibility in test

  def make_change(self, t1: str, t2: Union[str, List[str]]):
    
    # we dont use replace string method because is not prepared for overlapping matches
    pattern = rf"(?=({t1}))" # capturing group inside a lookahead matching overlapping patterns
    matches_idxs = [(m.start(1), m.end(1)) for m in re.finditer(pattern, self.text_in, re.IGNORECASE)] # all the matches indexes
    k = math.ceil( len(matches_idxs) * self.change_frq) # select the ceil of % of all matches
    rand_idxs = sorted(random.sample(matches_idxs, k = k), key = lambda x: x[0]) # select random indexes and ordered by aparition
    
    logger.info( f"Total number of matches = {len(matches_idxs)}, \n{25*' '} Number of changes done = {k}, \n{25*' '} All indexes matches: {matches_idxs}, \n{25*' '} Random indexes:{rand_idxs} ")
    init_len = len(self.text_in)
    for i, (idx_start, idx_end) in enumerate(rand_idxs): # apply the change in each idx selected
      shift_len = init_len - len(self.text_in) # take into account the shift made in idxs after each substitution
      if isinstance(t2, list):
        t2_selected = random.choice(t2) # select randomly a possible change
      else: 
        t2_selected = t2
      logger.info(f"Do change {i+1}: {t1} --> {t2_selected}")
      self.text_in = self.text_in[0:idx_start-shift_len] + t2_selected + self.text_in[idx_end-shift_len:]
    
    return self.text_in  


  def random_change(self, t1: str, t2: Union[str, List[str]]):
    n = random.random()
    if n <= self.change_prb:
      logger.info(f"All changes: {t1} --> {t2}")
      self.text_in = self.make_change(t1, t2)
      return self.text_in
      
    else:
      return self.text_in
  
  def text2leet(self):
    if self.mode == "basic":
      list_changes = basic_mode
    
    for t1, t2 in  list_changes:
      

      self.text_in = self.random_change(t1, t2)

    return self.text_in 


# TODO
## [x] Controlar lower o upper case --> re.IGNORECASE
## Añadir nuevos cambios 
## Organizar cambios por nivel
## [x] En español debo quitar los acentos para hacer la sustitucion --> Unidecode. Eliminamos siempre los acentos aunque no se haga cambio
