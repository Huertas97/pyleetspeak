from typing import Union, List
import random
import re
import math
import unidecode
from itertools import permutations, product
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s-%(levelname)s- %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

basic_mode = [("a", ["4", "@"]), ("e", "3"), ("i", "1"), ("o", "0"), ("u", "_")]


class LeetSpeaker(object):
    """[summary]

    Parameters:
        text_in ([type]):
          [description]
        text_out ([type]):
          Output text already formatted to leetspeak
        text_in ([type]):
          [description]
        text_in ([type]):
          [description]
        text_in ([type]):
          [description]
        text_in ([type]):
          [description]

    Methods:
        make_change
    """

    def __init__(
        self,
        text_in: str,
        change_prb: float = 0.8,  # Probabilidad de que se de un cambio
        change_frq: float = 0.5,  # Frecuencia del cambio en el texto
        mode: str = "basic",  # which kind of substitution should be applied
        seed: int = None,
        verbose: bool = False,
        get_all_combs: bool = False,  # Do all combinations or not
    ):
        self.text_in = unidecode.unidecode(text_in)
        self.text_out = unidecode.unidecode(text_in)
        self.change_prb = change_prb
        self.change_frq = change_frq
        self.mode = mode
        self.get_all_combs = get_all_combs
        self.init_len = len(text_in)
        if self.mode == "basic":
            self.list_changes = basic_mode

        if verbose == True:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.WARNING)

        # None for full random process, set seed for reproducibility in test
        random.seed(seed) if seed else random.seed()

    def make_change_of_type(self, text: str, t1: str, t2: Union[str, List[str]], change_idxs: List[int]):
        """Method used to randomly apply a change of an target term t1 to a new term t2 in different positions. In case t2 is a set of possible changes, one is selected randomly

        This method receives the indices of the output text where the substitution of t1 for t2 must occur.
        These indexes must be ordered by occurrence.
        The changes are dynamically applied to the output text (self.text_out)

        Args:
            t1 (str): Target term in the original text introduced.
            t2 (Union[str, List[str]]): New term that replaces target term. It is a leetspeak term. In case of set of terms, one is randomly selected
            change_idex (List[int]): List of indexes of output text where the change of t1 for t2 should be applied

        Returns:
            str: The modified original text introduced with the target term (t1) replaced by the leetspeak term (t2)
        """

        # apply the change in each idx selected
        # for i, (idx_start, idx_end) in enumerate(change_idxs):
        #     # take into account the shift made in idxs after each substitution
        #     shift_len = self.init_len - len(self.text_out)
        #     logger.info(f"Do change {i+1}: {t1} --> {t2_selected}")
        #     self.text_out = (
        #         self.text_out[0 : idx_start - shift_len]
        #         + t2_selected
        #         + self.text_out[idx_end - shift_len :]
        #     )

        # apply the change in each idx selected
        init_len = len(text)
        for i, (idx_start, idx_end) in enumerate(change_idxs):
            # take into account the shift made in idxs after each substitution
            shift_len = init_len - len(text)
            logger.info(f"Do change {i+1}: {t1} --> {t2}")
            text = (
                text[0 : idx_start - shift_len]
                + t2
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

            if isinstance(t2, list):
                # select randomly a possible change
                t2_selected = random.choice(t2)
            else:
                t2_selected = t2
              
            self.text_out = self.make_change_of_type(self.text_out, t1, t2_selected, rand_idxs)
            return self.text_out

        else:
            return self.text_out

    def find_all_matches(self, text,  t1, t2):
        """Esta función recibe el texto y busca todos los matches de un elemento t1 en
        la secuencia original. Devuelve todas las posiciones donde ha hecho match y
        los símbolos que pueden ir en esa posición (juntanto el término original t1 con
        todos los posibles cambios t2). t2 puede ser una cadena o una lista DEVUELVE DE UN SOLO TÉRMINO

        Args:
            t1 ([type]): [description]
            t2 ([type]): [description]

        Returns:
            [type]: [description]
        """

        pattern = rf"(?=({t1}))"  # capturing group inside a lookahead matching overlapping patterns
        matches_idxs = []
        matches_symbols = []
        # for m in re.finditer(pattern, self.text_in, re.IGNORECASE):
        #     matches_idxs.append((m.start(1), m.end(1)))
        #     matches_symbols.append((self.text_in[m.start(1) : m.end(1)], t2))

        if isinstance(t2, list):
          for m in re.finditer(pattern, text, re.IGNORECASE):
            matches_idxs.append( (m.start(1), m.end(1)) )
            t2_comb = [ (text[m.start(1):m.end(1)], t2_sub)  for t2_sub in t2   ]
            matches_symbols.append( t2_comb )
        else:
          for m in re.finditer(pattern, text, re.IGNORECASE):
            matches_idxs.append( (m.start(1), m.end(1)) )
            matches_symbols.append( [(text[m.start(1):m.end(1)], t2)] )

        return matches_idxs, matches_symbols

    def make_all_changes(self, text, matches_idxs, matches_symbols):
        """Esta función toma el texto inicial, las posiciones del texto inicial que hay que cambiar,
        y todos los símbolos posibles por cada posición. Realiza una combinación de todos los posibles
        cambios en una palabra teniendo en cuenta los posibles cambios por cada posición.
        Una vez obtenidas todas las combinaciones de cambios para el texto de entrada, realiza cada combinación
        en un bucle. En cada bucle se van haciendo los cambios pertinentes en el orde de aparición y se tiene en cuenta
        si se modifica la longitud del texto inicial si se hace un cambio en la posición previa.

        Args:
            matches_idxs ([type]): [description]
            matches_symbols ([type]): [description]

        Returns:
            [type]: [description]
        """

        init_len = len(text)
        # Make all posible combinations of changes for all position.
        all_leet_text = []
        # for comb in product(*matches_symbols):
        #     # REcorrer cada posición y hacerle el cambio

        #     leet_text = self.text_in
        #     assert len(matches_idxs) == len(matches_symbols)
        #     # apply the change in each idx selected
        #     for (idx_start, idx_end), t2_selected in zip(matches_idxs, comb):
        #         # take into account the shift made in idxs after each substitution
        #         shift_len = self.init_len - len(leet_text)
        #         leet_text = (
        #             leet_text[0 : idx_start - shift_len]
        #             + t2_selected
        #             + leet_text[idx_end - shift_len :]
        #         )
        #     all_leet_text.append(leet_text)

        combs = list(product(*matches_symbols)) # [(('A', '4'), ('o', '0'), ('a', '4')), (('A', '4'), ('o', '0'), ('a', '@'))]
        for comb in combs:
            for comb in product(*comb):
                # REcorrer cada posición y hacerle el cambio
                leet_text = text
                assert len(matches_idxs) == len(matches_symbols)
                # apply the change in each idx selected
                for (idx_start, idx_end), t2_selected in zip(matches_idxs, comb):
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

        if self.get_all_combs:  # tenemos que hacer todos los cambios posibles
            matches_idxs = []
            matches_symbols = []
            text = self.text_out
            for t1, t2 in self.list_changes:
                # get idxs and matched symbols
                idxs, symbols = self.find_all_matches(text, t1, t2)
                matches_idxs.append(idxs) if idxs else None
                matches_symbols.append(symbols) if symbols else None

            # Flat list with all the changes idx and symbols
            matches_idxs = [item for sublist in matches_idxs for item in sublist]
            matches_symbols = [item for sublist in matches_symbols for item in sublist]

            # Sort both list according to idxs positions
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

        # vamos 1 a 1 para aplicar el randomness a cada posible cambio
        else:
            for t1, t2 in self.list_changes:
                self.text_out = self.random_change(t1, t2)
            return self.text_out


# TODO
## Controlar lower o upper case
## Añadir nuevos cambios
## Organizar cambios por nivel
# Poder añadir manualmente cambios
# change frq puede ser aleatoria
# mejorar como se coge la lista de cambios
# organizar mejor el texto introducido.
