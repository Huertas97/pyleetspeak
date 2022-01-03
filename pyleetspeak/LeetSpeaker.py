from typing import Union, List
import random
import re
import math
import unidecode
from itertools import product
import logging
from modes import basic_mode
import copy
from collections import defaultdict

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
        text_in: str,
        change_prb: float = 0.8,
        change_frq: float = 0.5,
        mode: str = "basic",
        seed: int = None,
        verbose: bool = False,
        get_all_combs: bool = False,  # Do all combinations or not
        user_changes: list = None,
    ):
        self.text_in = unidecode.unidecode(text_in)
        self.text_out = unidecode.unidecode(text_in)
        self.change_prb = change_prb
        self.change_frq = change_frq
        self.mode = mode
        self.get_all_combs = get_all_combs
        self.init_len = len(text_in)

        # Select predefined changes
        if self.mode == "basic":
            self.list_changes = copy.deepcopy(basic_mode)

        # No pre-defined changes will be used
        elif self.mode == None:
            self.list_changes = []

        # Changes introduced by the user will be added to the predefined changes
        if user_changes:
            assert isinstance(user_changes, dict) or isinstance(user_changes, list)
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

    def make_change_of_type(
        self, text: str, t1: str, t2: Union[str, List[str]], change_idxs: List[int]
    ):
        """Method used to randomly apply a change of an target term t1 to a new term t2 in different positions. In case t2 is a set of possible changes, one is selected randomly

        This method receives the indices of the output text where the substitution of t1 for t2 must occur.
        These indexes must be ordered by occurrence.
        The changes are dynamically applied to the output text (self.text_out)

        Args:
            text (str): Text where the substitutions will take place.
            t1 (str): Target term in the original text introduced.
            t2 (Union[str, List[str]]): New term that replaces target term. It is a leetspeak term. In case of set of terms, one is randomly selected
            change_idex (List[int]): List of indexes of output text where the change of t1 for t2 should be applied

        Returns:
            str: The modified original text introduced with the target term (t1) replaced by the leetspeak term (t2)
        """

        # apply the change in each idx selected
        init_len = len(text)
        for i, (idx_start, idx_end) in enumerate(change_idxs):
            # take into account the shift made in idxs after each substitution
            shift_len = init_len - len(text)
            if isinstance(t2, list):
                # select randomly a possible change
                t2_selected = random.choice(t2)
            else:
                t2_selected = t2
            logger.info(f"Do change {i+1}: {t1} --> {t2_selected}")
            text = (
                text[0 : idx_start - shift_len]
                + t2_selected
                + text[idx_end - shift_len :]
            )

        return text

    def random_change(self, t1: str, t2: Union[str, List[str]]):
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
        n = random.random()
        if n <= self.change_prb:
            logger.info(f"All changes: {t1} --> {t2}")

            # we dont use replace string method because is not prepared for overlapping matches
            # capturing group inside a lookahead matching overlapping patterns
            # we search for the t1 term that will be substituted
            pattern = rf"(?=({t1}))"

            # all the matches indexes. Ignore upper or lower case
            matches_idxs = [
                (m.start(1), m.end(1))
                for m in re.finditer(pattern, self.text_out, re.IGNORECASE)
            ]

            # Select the ceil of % of all matches according to the frequency of change specified
            k = math.ceil(len(matches_idxs) * self.change_frq)

            # select random indexes and ordered by occurence
            rand_idxs = sorted(random.sample(matches_idxs, k=k), key=lambda x: x[0])
            logger.info(
                f"""Total number of matches = {len(matches_idxs)}, \n{25*' '}
                Number of changes done = {k}, \n{25*' '} All indexes matches: {matches_idxs}, \n{25*' '}
                Random indexes:{rand_idxs}"""
            )

            self.text_out = self.make_change_of_type(self.text_out, t1, t2, rand_idxs)
            return self.text_out

        else:
            return self.text_out

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

        pattern = rf"(?=({t1}))"  # capturing group inside a lookahead matching overlapping patterns
        matches_idxs = []
        matches_symbols = []

        # The behaviour is different if there are only one or several possible substitutions.
        # E.g. Input: leetspeaak;  Type sub: ("a", ["4", "@"]) --> Idx [(7, 8), (8, 9)] ; Symbols [[('a', '4'), ('a', '@')], [('a', '4'), ('a', '@')]]
        if isinstance(t2, list):
            for m in re.finditer(pattern, text, re.IGNORECASE):
                matches_idxs.append((m.start(1), m.end(1)))
                t2_comb = [(text[m.start(1) : m.end(1)], t2_sub) for t2_sub in t2]
                matches_symbols.append(t2_comb)
        # E.g. Input: leetspeaak;  Type sub: ("e", "3") --> Idx [(1, 2), (2, 3), (6, 7)] ; Symbols [[('e', '3')], [('e', '3')], [('e', '3')]]
        else:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                matches_idxs.append((m.start(1), m.end(1)))
                matches_symbols.append([(text[m.start(1) : m.end(1)], t2)])

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
                        leet_text[0 : idx_start - shift_len]
                        + t2_selected
                        + leet_text[idx_end - shift_len :]
                    )
                all_leet_text.append(leet_text)

        return all_leet_text

    def text2leet(self):
        """[summary]

        Returns:
            [type]: [description]
        """

        # Get all possible leetspeak versions
        if self.get_all_combs:  # tenemos que hacer todos los cambios posibles
            matches_idxs = []
            matches_symbols = []
            text = self.text_out

            # Extract all the possition suscteptible to be changed. Tuple the original chr and substitution chr
            # E.g. Input: leetspeaak;  Type sub: [ ("a", ["4", "@"]), ("e", "3") ]
            # Idx [(7, 8), (8, 9), (1, 2), (2, 3), (6, 7)]
            # Symbols [[('a', '4'), ('a', '@')], [('a', '4'), ('a', '@')], [('e', '3')], [('e', '3')], [('e', '3')]]
            for t1, t2 in self.list_changes:
                # get idxs and matched symbols
                idxs, symbols = self.find_all_matches(text, t1, t2)
                matches_idxs.extend(idxs) if idxs else None
                matches_symbols.extend(symbols) if symbols else None

            # If append instead of extend: Flat list with all the changes idx and symbols
            # matches_idxs = [item for sublist in matches_idxs for item in sublist]
            # matches_symbols = [item for sublist in matches_symbols for item in sublist]

            # Sort both list according to idxs positions
            # E.g. Input: leetspeaak;  Type sub: [ ("a", ["4", "@"]), ("e", "3") ]
            # Idx [(1, 2), (2, 3), (6, 7), (7, 8), (8, 9)]
            # Symbols [[('e', '3')], [('e', '3')], [('e', '3')], [('a', '4'), ('a', '@')], [('a', '4'), ('a', '@')]]
            matches_idxs, matches_symbols = map(
                list,
                zip(
                    *sorted(
                        zip(matches_idxs, matches_symbols), key=lambda pair: pair[0]
                    )
                ),
            )

            # Make all changes
            all_leet_text = self.make_all_changes(text, matches_idxs, matches_symbols)
            return all_leet_text

        # Obtain a random change
        else:
            for t1, t2 in self.list_changes:
                self.text_out = self.random_change(t1, t2)
            self.text_out = self.text_out
            return self.text_out


# TODO
# [x] Controlar lower o upper case
# [ ] Añadir nuevos cambios
# [x] Organizar cambios por nivel
# [x] Poder añadir manualmente cambios
# [x] change frq puede ser aleatoria
# [x] mejorar como se coge la lista de cambios --> Se coge desde un import y con deepcopy para no modificarlo
