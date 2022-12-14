import random
import pyphen
import warnings


class InversionCamouflage(object):
    """This object takes a text, separate it in syllabels, select two syllabels and invert them.

    Args:
        object ([type]): [description]
    """

    def __init__(
        self,
        seed: int = None,
    ):
        """
        Args:
            seed (int, optional): Seed for reproducible results. Defaults to None.
        """
        self.seed = seed
        # None for full random process, set seed for reproducibility in test
        random.seed(seed) if seed else random.seed()

    def text2inversion(self, text, lang: str, max_dist: int = 2, only_max_dist_inv: bool = True):
        """This method takes a text, separate it in syllabels, select two syllabels and invert them.

        The inversion output can be controlled using the max_dist and only_max_dist_inv parameters.
        If several inversions can be applied with the same parameter, a random one is selected and applied.

        max_dist (int): Maximum distance between syllabels for inversion. 
                        Example: If max_dist = 1 in "va-cu-na" only inversions va <--> cu ; cu <--> na will occur
                        If max_dist = 2 in "va-cu-na"  inversions va <--> cu ; cu <--> na ; va <--> na will occur

        only_max_dist_inv (bool): Indicates whether you want to obtain only the inversion of max_dist or choose among
                            all inversions with the smallest possible distances up to max_dist. 
                            If True only max_dist inversion is considered for randomly selection of inversion.
        """

        # Check the language exists and is available
        if lang not in pyphen.LANGUAGES.keys():
            raise RuntimeError(
                f"""Internal error - Unkown lang. The mode selected should be one of the followings:
            {list(pyphen.LANGUAGES.keys())}
            If you do not want to use any pre-defined mode set the mode to None. "basic" is the default mode.
            """
            )

        # Hyphenitator. Hyphenitate text and split by syllabels
        dict_hyphen = pyphen.Pyphen(lang=lang)
        hyphen_text = dict_hyphen.inserted(text)
        syllabels = hyphen_text.split("-")

        if len(syllabels) < 2:
            # Not enough syllabels to invert
            return text

        # Check maximum distance between syllabels to be inverted make sense
        if max_dist > len(syllabels)-1:
            warnings.warn(
                f"""You have selected a maximum distance between syllabels ({max_dist}) for inversion greater than the maximum distance between syllables in the word ({len(syllabels)-1}). Reducing `max_dist` maximum distance between syllables.""",
                RuntimeWarning
            )
            max_dist = len(syllabels)-1
        elif max_dist == 0:
            warnings.warn(
                f"""You have selected a maximum distance between syllabels ({max_dist}). No inversion will be applied""",
                RuntimeWarning
            )
            return text

        # Instead of making groups with the syllabels we will work with the idxs of each syllable
        syllabels_idxs = list(range(len(syllabels)))

        # Create groups of idxs from consecutive syllabels of max_dist.
        # Ex. In ["va", "cu", "na", "ción"] and max_dist=2 --> [[0, 2], [1, 3]]
        if only_max_dist_inv:
            all_group_syllabels = [[syllabels_idxs[i], syllabels_idxs[i+max_dist]]
                                   for i in range(len(syllabels_idxs)-1) if i <= len(syllabels_idxs)-1 - max_dist]

        # Create groups of idxs from consecutive syllabels up to max_dist.
        # Ex. In ["va", "cu", "na", "ción"] and max_dist=2 --> [[0, 1], [1, 2], [2, 3], [0, 2], [1, 3]]
        else:
            all_group_syllabels = []
            # at least max_dist = 1 --> max_len_group = 2
            for dist in range(1, max_dist+1):
                group_syllabels = [[syllabels_idxs[i], syllabels_idxs[i+dist]]
                                   for i in range(len(syllabels_idxs)-1) if i <= len(syllabels_idxs)-1 - dist]
                all_group_syllabels.extend(
                    group_syllabels) if group_syllabels else None

        # Select randomly one of the groups of possible inversion
        idxs = random.choice(all_group_syllabels)

        # Make inversion
        syllabels[idxs[0]], syllabels[idxs[-1]
                                      ] = syllabels[idxs[-1]], syllabels[idxs[0]]

        return "".join(syllabels)
