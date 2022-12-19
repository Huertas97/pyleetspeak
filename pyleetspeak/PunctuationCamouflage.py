from typing import Union, List
import random
import string
import pyphen
import warnings


class PunctuationCamouflage(object):
    """Class object that implements the word camouflage by injecting punctuation symbols inside a input text

    Args:
        object ([type]): [description]
    """

    def __init__(
        self,
        seed: int = None,
        uniform_change: bool = False,
        hyphenate: bool = False,
        word_splitting: bool = False,
        punctuation: List[str] = string.punctuation + " ",
        lang: str = "es",  # "en" total of 69
    ):
        """
        Args:
            seed (int, optional): Seed for reproducible results. Defaults to None.
            uniform_change (bool, optional): Determines if the same punctuation character should be used in all the position where punctuation is injected . Defaults to False.
            hyphenate (bool, optional): Determines if the punctuation symbols should be injected in syllables or hyphenate locations. Defaults to False.
            word_splitting (bool, optional): Determines if the puntuation symbols should be injected in all the possible positions. The final output depends also if `hypenate` or `uniform_change` are selected. Defaults to False.
            punctuation (List[str], optional): List of puntuation symbols to use for the camouflage injection. Defaults to string.punctuation+" ".
            lang (str, optional): Language to be used in the `hyphenate` process. Defaults to "es".
        """
        self.seed = seed
        # None for full random process, set seed for reproducibility in test
        random.seed(seed) if seed else random.seed()

        self.uniform_change = uniform_change
        self.hyphenate = hyphenate
        self.word_splitting = word_splitting
        self.punctuation = punctuation
        self.lang = lang

    def make_punct_injection(self, camo_text, punct_idxs, punct_symbs):
        """Method used to inject punctuation symbols at selected positions in a given text.

        This method receives the indixes and the punctuation symbols where the injection will take place.
        These indexes must be ordered by occurrence.
        The changes are dynamically applied to the input text.

        Args:
            camo_text (str): Input text to be punctuation camouflage
            punct_idxs (List[int]): List of indexes in the input text sorted by occurrence where the punctuation injection should be applied.
            punct_symbs (List[str]): List of punctuation symbols equally sorted as `punct_idxs` with the punct symbols that will be applied in each idx.

        Returns:
            [str]: Punctuation camouflaged text
        """
        init_len = len(camo_text)
        for punct_idx, punct_symb in zip(punct_idxs, punct_symbs):
            shift_len = init_len - len(camo_text)
            camo_text = (
                camo_text[0 : punct_idx - shift_len]
                + punct_symb
                + camo_text[punct_idx - shift_len :]
            )
        return camo_text

    def get_punct_injections(self, text, n_inj: int):
        """Method to obtain the indexes where the punctuation symbols will be injected as well as the symbols to be injected.

        Args:
            text (str): Input text to be punctuation camouflage
            n_inj (int): Number of punctuation injections desired. Ignored if `word_splitting` is selected. If greater than maximum injection is restricted to the maximum. Default = 2.
        Returns:
            punct_idxs (List[int]): List of indexes where the punctuation injection wil occur
            punct_symbs (List[str]): List of punct symbols to be injected in each index
        """
        if self.hyphenate:
            if self.lang not in pyphen.LANGUAGES.keys():
                raise RuntimeError(
                    f"""Internal error - Unkown lang. The mode selected should be one of the followings:
                {list(pyphen.LANGUAGES.keys())}
                If you do not want to use any pre-defined mode set the mode to None. "basic" is the default mode.
                """
                )
            dict_hyphen = pyphen.Pyphen(lang=self.lang)
            hyphen_idx = dict_hyphen.positions(text)

            if not hyphen_idx:  # empty list, no syllabels detected
                return None, None  # return empty results

            # if word_spliting select all the possitions to be injected
            if self.word_splitting:
                n_inj = len(hyphen_idx)

            if n_inj > len(hyphen_idx):
                warnings.warn(
                    f"""You have selected `hyphenate` = True with a number of punctuation marks to insert ({n_inj}) greater than the maximum number of positions to hyphenate ({len(hyphen_idx)}). Therefore, the number of punctuation to be inserted is reduced to the maximum number of positions to hyphenate. """,
                    RuntimeWarning,
                )
                n_inj = len(hyphen_idx)

            punct_idxs = random.sample(hyphen_idx, k=n_inj)

        else:
            # if word_spliting select all the possitions to be injected
            if self.word_splitting:
                n_inj = len(text)

            if n_inj > len(text):
                warnings.warn(
                    f"""You have selected a number of punctuation marks to insert ({n_inj}) greater than the maximum number of letters in the word ({len(text)}). Therefore, the number of punctuation to be inserted is reduced to the maximum number of positions to hyphenate. """,
                    RuntimeWarning,
                )
                n_inj = len(text)
            punct_idxs = random.sample(range(len(text)), k=n_inj)

        # Use the same punctuation symbol for all idxs to be injected
        if self.uniform_change:
            n_inj = 1
            # select one punct symbol and repeat it len(idxs) times
            punct_symbs = list(random.sample(self.punctuation, k=n_inj)) * len(
                punct_idxs
            )
        # Use different punctuation symbol for each idx to be injected
        else:
            if n_inj > len(self.punctuation):
                warnings.warn(
                    f"""You have selected a number of punctuation marks to insert ({n_inj}) greater than the maximum number of punctuation symbols ({len(self.punctuation)}). Therefore, the number of punctuation to be inserted is reduced to the maximum number of punctuation symbols. """,
                    RuntimeWarning,
                )
                n_inj = len(self.punctuation)
            punct_symbs = list(random.sample(self.punctuation, k=n_inj))

        # Sort by idxs
        punct_idxs, punct_symbs = map(
            list,
            zip(*sorted(zip(punct_idxs, punct_symbs), key=lambda pair: pair[0])),
        )

        return punct_idxs, punct_symbs

    def text2punctcamo(self, text: str, n_inj: int = 2):
        """Method that get the positions where the symbols will be injected as well as the symbols to be injected and apply the injection.

        Args:
            text (str): Input text to be punctuation camouflage
            n_inj (int): Number of punctuation injections desired. Ignored if `word_splitting` is selected. If greater than maximum injection is restricted to the maximum. Default to 2.

        Returns:
            [str]: Punctuation camouflaged text
        """
        punct_idxs, punct_symbs = self.get_punct_injections(text, n_inj)

        # None if hyphen is not possible.
        if punct_idxs and punct_symbs:
            camo_text = self.make_punct_injection(text, punct_idxs, punct_symbs)
            return camo_text

        # Return input text in that case
        else:
            return text
