from typing import Union, List
import random
import string
import pyphen
import warnings
import re
import math
import unidecode
from itertools import product
import logging
from .modes import (
    basic_mode,
    intermediate,
    advanced,
    covid_basic_word_camouflage,
    covid_intermediate_word_camouflage,
)
import copy
from collections import defaultdict
from tqdm.auto import tqdm

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s-%(levelname)s- %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


class LeetSpeaker(object):
    """
    Parameters:
        text_in ([type]):
          [description]
        text_out ([type]):
          Output text already formatted to leetspeak
        change_prb (int):
          Probability of applying each substitution type
        change_frq (int):
          determines how frequently substitution is applied
        mode (str):
          Determines  which kind of substitutios should be applied
        seed (int):
          Seed for reproducible results
        verbose (bool):
          Select code verbosity
        get_all_combs (bool):
          Get all possible leetspeak variations of the introduced text
        user_changes (Union[List, Dict]):
            Dict or List of tuples with additional changes introduced by the user.

    """

    def __init__(
        self,
        mode: str = "basic",
        change_prb: float = 0.8,
        change_frq: float = 0.5,
        seed: int = None,
        verbose: bool = False,
        get_all_combs: bool = False,  # Do all combinations or not
        user_changes: list = None,
        uniform_change: bool = False,
    ):
        # self.text_in = unidecode.unidecode(text_in)
        # self.text_out = unidecode.unidecode(text_in)
        self.change_prb = change_prb
        self.change_frq = change_frq
        self.mode = mode
        self.get_all_combs = get_all_combs
        self.uniform_change = uniform_change
        self.seed = seed

        # Select predefined changes
        if self.mode not in [
            "basic",
            "intermediate",
            "advanced",
            "covid_basic",
            "covid_intermediate",
            None,
        ]:
            raise RuntimeError(
                f"""Internal error - Unkown mode: {self.mode}. The mode selected should be one of the followings:
            "basic", "intermediate", "advanced", "covid_basic", "covid_intermediate", None
            If you do not want to use any pre-defined mode set the mode to None. "basic" is the default mode.
            """
            )
        if self.mode == "basic":
            self.list_changes = copy.deepcopy(basic_mode)
        elif self.mode == "intermediate":
            self.list_changes = copy.deepcopy(intermediate)
        elif self.mode == "advanced":
            self.list_changes = copy.deepcopy(advanced)
        elif self.mode == "covid_basic":
            self.list_changes = copy.deepcopy(covid_basic_word_camouflage)
        elif self.mode == "covid_intermediate":
            self.list_changes = copy.deepcopy(
                covid_intermediate_word_camouflage)
        # No pre-defined changes will be used
        elif self.mode == None:
            self.list_changes = []

        # Changes introduced by the user will be added to the predefined changes
        if user_changes:
            assert isinstance(user_changes, dict) or isinstance(
                user_changes, list)
            self.user_changes = user_changes
            self.list_changes = self.add_user_changes()

        if verbose == True:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.WARNING)

        # None for full random process, set seed for reproducibility in test
        random.seed(seed) if seed else random.seed()

    def add_user_changes(self):
        """Method for combining pre-defined and user-defined substitution types

        Returns:
            List[Tuple]: List of tuples where each tuple is a substitution type. The first tuple
                        element is the target character and the second element is a list of possible substitution characters
        """
        # transform predefined changes into a dictionary
        chg_dict = dict(self.list_changes)

        # If changes introduced by user is not a dict transform it
        if not isinstance(self.user_changes, dict):
            self.user_changes = dict(self.user_changes)

        # Create a Defaultdict with type list for combining both dictionaries
        dd = defaultdict(list)
        for d in (chg_dict, self.user_changes):
            for key, value in d.items():
                dd[key].extend(value)

        # backtransform it to a list of tuples
        return [(k, v) for k, v in dd.items()]

    def make_change(self, text, change_idxs, change_chrs):
        """Method used to randomly apply a change of an target term t1 to a new term t2 in different positions. In case t2 is a set of possible changes, one is selected randomly

        This method receives the indices of the output text where the substitution of t1 for t2 must occur.
        These indexes must be ordered by occurrence.
        The changes are dynamically applied to the input text.

        Args:
            text (str): Text where the substitutions will take place.
            t1 (str): Target term in the original text introduced.
            t2 (Union[str, List[str]]): New term that replaces target term. It is a leetspeak term. In case of set of terms, one is randomly selected
            change_idex (List[int]): List of indexes of output text where the change of t1 for t2 should be applied

        Returns:
            str: The modified original text introduced with the target term (t1) replaced by the leetspeak term (t2)
        """
        init_len = len(text)
        for (idx_start, idx_end), t2_selected in zip(change_idxs, change_chrs):
            # take into account the shift made in idxs after each substitution
            shift_len = init_len - len(text)
            text = (
                text[0: idx_start - shift_len]
                + t2_selected
                + text[idx_end - shift_len:]
            )
        return text

    def get_all_changes_random(self, text, t1, t2):
        """Method to apply a substitution type to the original text if a threshold is randomly exceeded using the probability of change specified.

        A number between [0, 1] is randomly selected. If the number selected is equal or
        lower to the probability of change specified (change_prb), the substitution type is applied.
        Otherwise the substitution is not applied. If the threshold is exceeded the following steps are applied.
        Firstly, this method search for all the indexes thath match the target term (t1), including overlapping
        matches and ignoring upper or lowercase. Then, it selects the number of replacements of t1 by t2 according
        to the frequency of change specified (change_frq). Once the number of substitutions is selected, a random
        sample of all matches indexes are selected and ordered by occurence. This random indexes are passed to ´make_change´
        to make the substitutions.

        Args:
            t1 (str): Target term in the original text introduced.
            t2 (Union[str, List[str]]): New term that replaces target term. It is a leetspeak term. In case of set of terms, one is randomly selected

        Returns:
            str: The modified original text introduced with the target term (t1) replaced by the leetspeak term (t2)
        """
        matches_idxs = []
        matches_symbols = []
        n = random.random()
        if n <= self.change_prb:
            # we dont use replace string method because is not prepared for overlapping matches
            # capturing group inside a lookahead matching overlapping patterns
            # we search for the t1 term that will be substituted
            pattern = rf"(?=({t1}))"

            # If uniform_change is selected, randomly select the subs chr for the same target chr
            # If there are several possible substitutions and we want to apply in all cases the same substitution
            if isinstance(t2, list) and self.uniform_change:
                t2_choice = random.choice(t2)

            # all the matches indexes. Ignore upper or lower case
            for m in re.finditer(pattern, text, re.IGNORECASE):
                matches_idxs.append((m.start(1), m.end(1)))

                if isinstance(t2, list):
                    # select t2_choice randomly independent between matches for the same target chr
                    if not self.uniform_change:
                        t2_choice = random.choice(t2)
                        matches_symbols.append(t2_choice)
                    # already t2_choice was uniformingly selected
                    else:
                        matches_symbols.append(t2_choice)
                else:
                    matches_symbols.append(t2)

            # Only if the target chr (t1) has been found
            if matches_idxs:
                # Select the ceil of % of all matches according to the frequency of change specified
                k = math.ceil(len(matches_idxs) * self.change_frq)
                rand_lists = random.sample(
                    list(zip(matches_idxs, matches_symbols)), k=k
                )

                matches_idxs, matches_symbols = zip(*rand_lists)
                matches_idxs, matches_symbols = list(matches_idxs), list(
                    matches_symbols
                )

        return matches_idxs, matches_symbols

    def find_all_matches(self, text, t1, t2):
        """Extract all the possition suscteptible to be changed. Return a tuple with the original chr and substitution chr

        Args:
            text (str): Text where the substitutions will take place.
            t1 (str): Target term in the original text introduced.
            t2 (Union[str, List[str]]): New term that replaces target term. It is a leetspeak term. In case of set of terms, one is randomly selected

        Returns:
            matches_idxs (List[Tuple]): List of tuples where each tuple are the indexes to be changed
            matches_symbols (List[List[Tuple]]): Possible character in a certain index (is equally sorted as maches_idxa).
                                                 Each tuple contains the original character and the substituion character.
                                                 Each sublist will contain a tuple for each substitution characters that
                                                 can be applied.
        """

        # capturing group inside a lookahead matching overlapping patterns
        pattern = rf"(?=({t1}))"
        matches_idxs = []
        matches_symbols = []

        # The behaviour is different if there are only one or several possible substitutions.
        # E.g. Input: leetspeaak;  Type sub: ("a", ["4", "@"]) --> Idx [(7, 8), (8, 9)] ; Symbols [[('a', '4'), ('a', '@')], [('a', '4'), ('a', '@')]]
        if isinstance(t2, list):
            for m in re.finditer(pattern, text, re.IGNORECASE):
                matches_idxs.append((m.start(1), m.end(1)))
                t2_comb = [(text[m.start(1): m.end(1)], t2_sub)
                           for t2_sub in t2]
                matches_symbols.append(t2_comb)
        # E.g. Input: leetspeaak;  Type sub: ("e", "3") --> Idx [(1, 2), (2, 3), (6, 7)] ; Symbols [[('e', '3')], [('e', '3')], [('e', '3')]]
        else:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                matches_idxs.append((m.start(1), m.end(1)))
                matches_symbols.append([(text[m.start(1): m.end(1)], t2)])

        return matches_idxs, matches_symbols

    def split_list_changes(self, list_of_changes):
        """This function splits a list of changes where into sublists of simplier changes.

        This function is only applied for 'uniform_changes' == True. The input consists of a List[Tuple], where each tuple is a type of
        change. In each tuple there are two elements, the first one is the target character to be replaced and the second element is a
        chr or a list of characters to use in the substitution. This method create simplier list of changes, one for each element in the
        second list element. Therefore, from a list with several changes for a type of substitution we obtain several list of changes each
        one only with one substitution character for each tuple.
        """
        # We will create all combinations between substitution (values of dict), preserving the keys
        # - keys: original/target characters   - values: substitution characters
        keys, values = zip(*dict(list_of_changes).items())

        # Create all combination of different substitution types
        # [('4', '3', '1', '0', '_'), ('@', '3', '1', '0', '_')]
        subs_combs = list(product(*values))

        # Backtransform each combination of substitutions into a list of tuples with the original character
        # [ [('a', '4'), ('e', '3'), ('i', '1'), ('o', '0'), ('u', '_')], [('a', '@'), ('e', '3'), ('i', '1'), ('o', '0'), ('u', '_')] ]
        return [[(k, v) for k, v in zip(keys, subs_comb)] for subs_comb in subs_combs]

    def get_all_changes(self, text_in, list_of_changes):
        """Esta función obtiene todos los indices donde se ha encontrado un match y debería hacerse un cambio.
           Además devuelve en una tupla el elemento que debe sustituirse y por el cual debe sustituirse

        Args:
            changes (List[Tuple]): Lista con los cambios que se han de realizar. Cada tipo de cambio está en una tupla.
                                El primer elemento de la tupla es el elemento a sustituir y el segundo elemento el
                                caracter por el cual ha de substituirse. Este segundo elemento puede ser una lista

        Returns:
            matches_idxs:
            matches_symbols:
        """
        matches_idxs = []
        matches_symbols = []
        # Extract all the possition suscteptible to be changed. Tuple the original chr and substitution chr
        # E.g. Input: leetspeaak;  Type sub: [ ("a", ["4", "@"]), ("e", "3") ]
        # Idx [(7, 8), (8, 9), (1, 2), (2, 3), (6, 7)]
        # Symbols [[('a', '4'), ('a', '@')], [('a', '4'), ('a', '@')], [('e', '3')], [('e', '3')], [('e', '3')]]
        for change in list_of_changes:
            t1, t2 = change
            idxs, symbols = self.find_all_matches(text_in, t1, t2)
            matches_idxs.extend(
                idxs) if idxs and idxs[0] not in matches_idxs else None
            matches_symbols.extend(symbols) if symbols else None

        # Sort both list according to idxs positions
        # E.g. Input: leetspeaak;  Type sub: [ ("a", ["4", "@"]), ("e", "3") ]
        # Idx [(1, 2), (2, 3), (6, 7), (7, 8), (8, 9)]
        # Symbols [[('e', '3')], [('e', '3')], [('e', '3')], [('a', '4'), ('a', '@')], [('a', '4'), ('a', '@')]]
        matches_idxs, matches_symbols = map(
            list,
            zip(*sorted(zip(matches_idxs, matches_symbols),
                key=lambda pair: pair[0])),
        )
        return matches_idxs, matches_symbols

    def make_all_changes(self, text, matches_idxs, matches_symbols):
        """Method in charge of get all possible combinations of substitutions from a text

        This method takes the initial text, the indexes susceptible of being changed, and the
        characters for each position (`matches_symbols`). To obtain the final output, it applies two
        combination processes.
        Firstly, it gets all the combination of tuples between different sublist of `matches_symbols`.
        Secondly, it combines these combinations to obtain all the possible character in each position,
        combining original and substitution characters. Finally, Loop through each idx and each change
        in character combinations and apply the change

        Args:
            text (str): Text where the substitutions will take place.
            matches_idxs (List[Tuple]): List of tuples where each tuple are the indexes to be changed
            matches_symbols (List[List[Tuple]]): Possible character in a certain index (is equally sorted as maches_idxa).
                                                 Each tuple contains the original character and the substituion character.
                                                 Each sublist will contain a tuple for each substitution characters that
                                                 can be applied.

        Returns:
            List[str]: List with all the leetspeak variation of a introduced text
        """

        init_len = len(text)
        all_leet_text = []

        # Only symbols are combined, because idxs remain the same
        # Make all posible combinations of substitution characters (second element of tuple)
        # E.g. Input: leetspeaak;  Type sub: [ ("a", ["4", "@"]), ("e", "3") ]
        # Idx [(1, 2), (2, 3), (6, 7), (7, 8), (8, 9)]
        # First Chr Comb: (('e', '3'), ('e', '3'), ('e', '3'), ('a', '4'), ('a', '4'))
        # Second Chr Comb: (('e', '3'), ('e', '3'), ('e', '3'), ('a', '4'), ('a', '@')) ...
        chr_combs = list(product(*matches_symbols))

        for comb in chr_combs:
            # Get all combinations between tuples
            # E.g. Input: leetspeaak;  Type sub: [ ("a", ["4", "@"]), ("e", "3") ]
            # Idx [(1, 2), (2, 3), (6, 7), (7, 8), (8, 9)]
            # First Comb: (('e', '3'), ('e', '3'), ('e', '3'), ('a', '4'), ('a', '4'))
            # First Element Product Comb: ('e', 'e', 'e', 'a', 'a')
            # Second Element Product Comb: ('e', 'e', 'e', 'a', '4') ...
            for chr_comb_comb in product(*comb):
                leet_text = text
                assert len(matches_idxs) == len(matches_symbols)

                # Loop through each idx and each change in character combinations and apply the change
                # Both lists should be equally sorted
                for (idx_start, idx_end), t2_selected in zip(
                    matches_idxs, chr_comb_comb
                ):
                    # take into account the shift made in idxs after each substitution
                    shift_len = init_len - len(leet_text)
                    leet_text = (
                        leet_text[0: idx_start - shift_len]
                        + t2_selected
                        + leet_text[idx_end - shift_len:]
                    )
                all_leet_text.append(leet_text)

        return all_leet_text

    def text2leet(
        self,
        text_in,
    ):
        """[summary]

        Returns:
            [type]: [description]
        """
        text_in = unidecode.unidecode(text_in)
        self.text_in = text_in

        # Get all possible leetspeak versions
        if self.get_all_combs:  # tenemos que hacer todos los cambios posibles
            # Get all combinations but applying the same substitution character for each substitution type
            if self.uniform_change:
                # Split a complex list of changes (several subs character for each subs type) into
                # a simpler one (only one subs chr for each subs type)
                all_list_changes = self.split_list_changes(self.list_changes)

                all_leet_text = []
                # Apply the changes for each list of changes independently but merge the results
                for changes in all_list_changes:
                    # Get all idxs where to apply a change and the substitution for each idx
                    matches_idxs, matches_symbols = self.get_all_changes(
                        text_in, changes
                    )
                    # Make all changes
                    result_leet_text = self.make_all_changes(
                        text_in, matches_idxs, matches_symbols
                    )
                    all_leet_text.extend(result_leet_text)

            # Get all combinations combining different subs chrs for the same subs type in different idxs
            else:
                all_leet_text = []
                # Get all idxs where to apply a change and the substitution for each idx
                matches_idxs, matches_symbols = self.get_all_changes(
                    text_in, self.list_changes
                )
                # Make all changes
                all_leet_text = self.make_all_changes(
                    text_in, matches_idxs, matches_symbols
                )

            # Remove duplicates (only when no subs character is applied is repeated)
            all_leet_text = list(set(all_leet_text))
            return all_leet_text

        # Obtain a random change
        else:
            all_matches_idxs = []
            all_matches_symbols = []
            for t1, t2 in self.list_changes:
                matches_idxs, matches_symbols = self.get_all_changes_random(
                    text_in, t1, t2
                )
                all_matches_idxs.extend(matches_idxs) if matches_idxs else None
                all_matches_symbols.extend(
                    matches_symbols) if matches_symbols else None

            if all_matches_idxs and all_matches_symbols:
                all_matches_idxs, all_matches_symbols = map(
                    list,
                    zip(
                        *sorted(
                            zip(all_matches_idxs, all_matches_symbols),
                            key=lambda pair: pair[0],
                        )
                    ),
                )
                text_out = self.make_change(
                    text_in, all_matches_idxs, all_matches_symbols
                )
            else:
                text_out = text_in

            self.text_out = text_out
            return text_out


# TODO
# [x] Controlar lower o upper case
# [x] Añadir nuevos cambios
# [x] Organizar cambios por nivel
# [x] Poder añadir manualmente cambios
# [x] change frq puede ser aleatoria
# [x] mejorar como se coge la lista de cambios --> Se coge desde un import y con deepcopy para no modificarlo
# [ ] que el usuario indique la probabilidad de un cambio
# [x] Text_in que no esté en init. Objeto con parámetros de cambio
# [x] Manejar la situación en la que el modo no esté definido correctamente --> se indica cuales están disponibles
# [x] Muy habitualmente se emplea el mismo cambio para el mismo caracter. Es decir, meterle la posibilidad de que sólo
# se eliga un tipo de sustitución para cada tipo de cambio --> uniform_changes ha sido incorporado en caso random y get_all_comb
# [ ] Preparar modificaciones que implican espacios. Ver lo en el inforde de disinfolab EU
# [ ] Hacer más eficiente el obtener todas las combinaciones uniformes. Tarda más que obteniendo todas.

# COMODINES
# [ ] Añadir * y '' (de eliminar) a todas las combinaciones. Hay una serie de símbolos comodines que son comunes
# para varias letras. Podemos añadirlas en todos los cambios. Pero también podemos darle menos prob de salir. Habría
# que dar esa posibilidad.
# Comodines Vocales --> "*", "", "/",  "_"
# Las consonantes no suelen desaparecer


# Punctuation WORD CAMOUFLAGE
# Tenemos varios metodos !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~

# [x] 1 - Single random/syllable injection - Meter un simbolo de puntuacion en una posicion aleatoria de la palabra.
# Añadir modo sílaba, que inserte entre silabas. Multilingual hypenithation algrithms: https://pypi.org/project/pyphen/
# Ej: COVID --> CO_VID, COV_ID, COV ID, C#OVID

# [x] 2 - Multiple random/syllable injection - Meter un simbolo de puntuacion en dos o mas posiciones de la palabra (seleccion aleatoria de la pos y el número).
# Incorporar uniform_change.  Añadir modo sílaba, que inserte entre silabas. Multilingual hypenithation algrithms: https://pypi.org/project/pyphen/
# Ej. plandemia --> #plan#demia, plan#de#mia, pla_nde_mia, plan##demia, p##lan##demia, plan#de_mia

# [x] 3 - Word splitting/syllable - Separamos todas las letras de una palabra por simbolos de puntuacion.  Incorporar uniform_change
# Ej. Vacuna --> v-a-c-u-n-a, v_a_c_u_n_a, v.a.c.u.n.a, v.a.c_u.n.a


# INVERSION
# Partir la palabra en silabas e intercambiar dos de ellas.
# Multilingual hypenithation algrithms: https://pypi.org/project/pyphen/
# Ej. Vacuna --> nacuva

# Combinar Word Camouflage y LeetSpeak
# El Punctuation word camouflage está centrado en emplear símbolos de puntuación para camuflar la palabra. Mientras que el leetspeak emplea sustituciones
# para camuflar la palabra.
# De este modo son compatibles, pero yo lo organizaría de la siguiente manera. Primero se haría leetspeak y luego puntuation camouflage.
# Solo que se asignaría una probabilidad de que se aplique cada uno de estos pasos. Aleatoriamente se decidiría si se hace el primero,
# el segundo, ninguno o ambos pasos.
# El primer ejemplo emplea las dos, pero el segundo solo leetspek
# Ej  b4.cu.n4s (vaccines) k0vbld (Covid),
