from .PunctuationCamouflage import PunctuationCamouflage
from .InversionCamouflage import InversionCamouflage
from .LeetSpeaker import LeetSpeaker
from collections import OrderedDict
from codetiming import Timer
from typing import Union, List, Tuple
import numpy as np
import re
from keybert import KeyBERT
import random
import itertools
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import yake

languages_codes_nltk = {
    "es": "spanish",
    "fr": "french",
    "nl": "dutch",
    "it": "italian",
    "fi": "finnish",
    "de": "german",
    "sv": "swedish",
    "en": "english",
    "sl": "slovene",
    "ne": "nepali",
    "el": "greek",
    "nb": "norwegian",
    "ru": "russian",
    "pt": "portuguese",
    "da": "danish",
    "tr": "turkish",
    "tg": "tajik",
    "hu": "hungarian",
    "id": "indonesian",
    "az": "azerbaijani",
    "ro": "romanian",
    "ar": "arabic",
    "kk": "kazakh",
    # Additional
    # "bg": "bulgarian",
    # "ga": "irish",
    # "hr": "croatian",
    # "lt": "lithuanian",
    # "lv": "latvian",
    # "pl": "polish",
    # "sk": "slovak"
}


class augmenter(object):
    """
    Class to perform word camouflage augmentation. Similar to NER_data_generator, but for text augmentation where you
    can customize in-depth the behaviour of the word camouflage process.
    """

    def __init__(
        self,
        extractor_type: str,  # "yake" or "keybert",
        # KeyBERT parameters
        kw_model_name: str = "AIDA-UPM/mstsb-paraphrase-multilingual-mpnet-base-v2",
        max_top_n: int = 5,
        seed: int = None,
        lang: str = "en",
        # LeetSpeaker parameters
        leet_mode: str = None,  # Mode of leetspeak. If none, random mode is applied
        leet_change_prb: float = 0.8,
        leet_change_frq: float = 0.5,
        # Probability oof applying uniform change in leetspeak
        leet_uniform_change: float = 0.6,
        # PunctuationCamouflage parameters
        punt_hyphenate_prb=0.5,
        punt_uniform_change_prb=0.6,
        punt_word_splitting_prb=0.5,
        # InversionCamouflage parameters
        inv_max_dist=4,
        inv_only_max_dist_prb=0.5,
        # Probability of applying leetspeak or punct camo. If not, inversion camo is applied
        leet_punt_prb: float = 0.9,
        # Probability of word camouflaging techniques when inversion is not applied
        leet_prb=0.45,
        punct_prb=0.25,
        leet_basic_punt_prb=0.15,
        leet_covid_basic_punt_prb=0.15,
    ):
        """
        :param extractor_type: Type of extractor to use. "yake" or "keybert".
        :param kw_model_name: Name of the keyword extraction model for KeyBERT. Default: AIDA-UPM/mstsb-paraphrase-multilingual-mpnet-base-v2
        :param max_top_n: Maximum number of keywords to extract from the sentence. Default: 5
        :param seed: Seed for reproducibility. Default: None
        :param lang: Language of the sentence. Default: "en"
        :param leet_punt_prb: Probability of applying leetspeak or punct camo. If not, inversion camo is applied. Default: 0.9
        :param leet_mode: Mode of leetspeak. If none, random mode is applied. Default: None
        :param leet_change_prb: Probability of changing a character in leetspeak. Default: 0.8
        :param leet_change_frq: Frequency of changing a character in leetspeak. Default: 0.5
        :param leet_uniform_change: Probability of applying uniform change in leetspeak. Default: 0.6
        :param p_hyphenate_prb: Probability of hyphenating a word. Default: 0.5
        :param p_uniform_change_prb: Probability of applying uniform change in punctuation. Default: 0.6
        :param p_word_splitting_prb: Probability of splitting a word. Default: 0.5
        :param inv_max_dist: Maximum distance between words to invert. Default: 4
        :param inv_only_max_dist_prb: Probability of applying inversion only to words with maximum distance. Default: 0.5
        :param leet_prb: Probability of applying leetspeak when inversion is not applied. Default: 0.45
        :param punct_prb: Probability of applying punctuation camouflage when inversion is not applied. Default: 0.25
        :param leet_basic_punt_prb: Probability of applying leetspeak or punctuation camouflage when inversion is not applied. Default: 0.15
        :param leet_covid_basic_punt_prb: Probability of applying leetspeak or punctuation camouflage when inversion is not applied. Default: 0.15
        """
        self.extractor_type = extractor_type
        self.max_top_n = max_top_n
        self.lang = lang

        if self.extractor_type == "yake":
            self.yake_extractor = yake.KeywordExtractor(
                lan=self.lang,
                n=1,  # Number of words in the keyword
                dedupLim=0.9,  # Deduplication limit
                dedupFunc="seqm",  # Deduplication function
                windowsSize=1,  # Window size, used for deduplication purposes
                top=self.max_top_n,  # Number of keywords to be returned
                features=None,  # Features to be used for weighting the keywords.
            )
        elif self.extractor_type == "keybert":
            self.kw_model = KeyBERT(model=kw_model_name)

        self.leet_punt_prb = leet_punt_prb
        # self.leet_mode = leet_mode
        self.leet_change_prb = leet_change_prb
        self.leet_change_frq = leet_change_frq
        self.leet_uniform_change = leet_uniform_change
        self.punt_hyphenate_prb = punt_hyphenate_prb
        self.punt_uniform_change_prb = punt_uniform_change_prb
        self.punt_word_splitting_prb = punt_word_splitting_prb
        self.inv_max_dist = inv_max_dist
        self.inv_only_max_dist_prb = inv_only_max_dist_prb
        self.leet_prb = leet_prb
        self.punct_prb = punct_prb
        self.leet_basic_punt_prb = leet_basic_punt_prb
        self.leet_covid_basic_punt_prb = leet_covid_basic_punt_prb

        self.seed = seed
        # None for full random process, set seed for reproducibility in test
        random.seed(self.seed) if seed else random.seed()
        if seed:
            rng = np.random.RandomState(seed)
        else:
            rng = np.random.RandomState()
        self.rng = rng

    def get_keywords(
        self, sentence, stop_words, keyphrase_ngram_range, important_kws, **kwargs
    ):
        # if stopwords are not a list of stopwords, a pre-defined nltk list will be used
        if isinstance(stop_words, str):
            if stop_words not in list(languages_codes_nltk.keys()):
                raise RuntimeError(
                    f"Language selected not available. Please select one of the follolowing: {list(languages_codes_nltk.keys())}"
                )
            else:
                stop_words = stopwords.words(languages_codes_nltk[stop_words])

        # Compute keyBERT
        num_words = len(word_tokenize(sentence))

        # limit the number of keywords
        if num_words < 10:
            n_kw = random.randint(1, 2)
        else:
            n_kw = random.randint(1, self.max_top_n)

        if self.extractor_type == "yake":
            kws = self.yake_extractor.extract_keywords(sentence)

        elif self.extractor_type == "keybert":
            kws = self.kw_model.extract_keywords(
                sentence,
                stop_words=stop_words,
                keyphrase_ngram_range=keyphrase_ngram_range,
                top_n=n_kw,
                **kwargs,
            )

        kws = [kw for kw, sim_score in kws]

        if important_kws:
            pattern = re.compile("|".join(important_kws), re.IGNORECASE)
            important_kws_find = re.findall(pattern, sentence)
            [
                kws.append(imp_kw.lower())
                for imp_kw in important_kws_find
                if imp_kw.lower() not in kws
            ]

        return kws

    def idxs_overlap(self, idx_1, idx_2):
        # Get two tuples (representing idxs) and get if they overlap.
        # considering the ranges are: [x1:x2] and [y1:y2]
        x1, x2 = idx_1
        y1, y2 = idx_2
        return x1 <= y2 and y1 <= x2

    def filter_overlapping(self, ori_data):
        # Filter overlapping matches. If overlaps get the larger one
        list_idxs = [dict_in["init_idxs"] for dict_in in ori_data["meta"]]

        # generate all possible combinations of 2 idxs
        delete_overlapping_rg = []
        for a, b in itertools.combinations(list_idxs, 2):
            # check if they overlap
            if self.idxs_overlap(a, b):
                # Discar the smaller one
                if a[1] - a[0] > b[1] - b[0]:
                    delete_overlapping_rg.append(b)
                else:
                    delete_overlapping_rg.append(a)

        # Get the idxs of the sublist of all matches that are not discarded
        selected_idxs = [
            i for i, e in enumerate(list_idxs) if e not in delete_overlapping_rg
        ]

        # Extract only the selected matches taht do not overlap or if overlap are the larger one
        ori_data["meta"] = [
            dict_in for i, dict_in in enumerate(ori_data["meta"]) if i in selected_idxs
        ]
        return ori_data

    def get_new_idxs(self, kw_in, kw_leet, ori_idx, shift):
        end_ori = ori_idx[-1]
        shift = len(kw_leet) - len(kw_in) + shift
        end_leet = end_ori + shift
        start_leet = end_leet - len(kw_leet)
        return (start_leet, end_leet), shift

    def leet_replacement(self, ori_data: dict):
        leet_kws = [i["kw_leet"] for i in ori_data["meta"]]
        ori_idxs = [i["init_idxs"] for i in ori_data["meta"]]
        leet_idxs = [i["leet_idxs"] for i in ori_data["meta"]]
        new_s = ori_data["sentence"]
        init_len = len(new_s)

        for init_idxs, leet_kw in zip(ori_idxs, leet_kws):
            shift_len = init_len - len(new_s)
            start_ori, end_ori = init_idxs
            new_s = (
                new_s[: start_ori - shift_len] + leet_kw + new_s[end_ori - shift_len :]
            )

        # Check leet idxs match with kw_leet in leet_sent
        for leet_kw, leet_idx in zip(leet_kws, leet_idxs):
            assert (
                leet_kw == new_s[leet_idx[0] : leet_idx[1]]
            ), "Leet kws inserted do not match with Leet indexes"

        return new_s

    def get_random_method(self):
        # Probability of applyinh leetspeak or punct camouflage
        num = self.rng.rand()
        if num <= self.leet_punt_prb:
            methods = [
                ["leetspeak"],
                ["punct_camo"],
                ["leetspeak-basic", "punct_camo"],
                ["leetspeak-covid_basic", "punct_camo"],
            ]
            method_idx = self.rng.choice(
                [0, 1, 2, 3],
                size=1,
                replace=False,
                p=[
                    self.leet_prb,
                    self.punct_prb,
                    self.leet_basic_punt_prb,
                    self.leet_covid_basic_punt_prb,
                ],
            ).squeeze()
            method = methods[method_idx]

        else:
            method = ["inv_camo"]

        return method

    def get_random_leetspeak(self, mode: str = None):
        # Randomly select parameters value
        if not mode:  # leetspeak is random with no punct camouflage
            modes = [
                "basic",
                "covid_basic",
                "intermediate",
                "covid_intermediate",
                "advanced",
            ]
            mode = self.rng.choice(
                modes, size=1, replace=False, p=[0.25, 0.25, 0.2, 0.2, 0.1]
            ).squeeze()
        uniform_change = self.rng.choice(
            [True, False],
            size=1,
            replace=False,
            p=[self.leet_uniform_change, 1 - self.leet_uniform_change],
        ).squeeze()

        leeter = LeetSpeaker(
            change_prb=self.leet_change_prb,
            change_frq=self.leet_change_frq,
            mode=mode,
            seed=self.seed,  # for reproducibility purposes
            get_all_combs=False,
            uniform_change=uniform_change,
        )
        return leeter

    def get_random_punt_camo(self):
        # Randomly select parameters value
        hyphenate = self.rng.choice(
            [True, False],
            size=1,
            replace=False,
            p=[self.punt_hyphenate_prb, 1 - self.punt_hyphenate_prb],
        ).squeeze()
        uniform_change = self.rng.choice(
            [True, False],
            size=1,
            replace=False,
            p=[self.punt_uniform_change_prb, 1 - self.punt_uniform_change_prb],
        ).squeeze()
        word_splitting = self.rng.choice(
            [True, False],
            size=1,
            replace=False,
            p=[self.punt_word_splitting_prb, 1 - self.punt_word_splitting_prb],
        ).squeeze()

        punt_camo = PunctuationCamouflage(
            word_splitting=word_splitting,
            uniform_change=uniform_change,
            hyphenate=hyphenate,
            lang=self.lang,
            seed=self.seed,  # for reproducibility
        )
        return punt_camo

    def get_params_inverter(self):
        # Randomly select parameters value
        max_dist = self.rng.randint(1, self.inv_max_dist)
        only_max_dist_inv = self.rng.choice(
            [True, False],
            size=1,
            replace=False,
            p=[self.inv_only_max_dist_prb, 1 - self.inv_only_max_dist_prb],
        ).squeeze()
        params = {}
        params["lang"] = self.lang
        params["max_dist"] = max_dist
        params["only_max_dist_inv"] = only_max_dist_inv
        return params

    def apply_leetspeak(self, kw):

        # if kw to camouflage is <=1 return None because no change will be applied
        # if len(kw) <= 1:
        #   return None

        method_tag = list(self.get_random_method())

        leet_kw = kw
        # print("Leet kw -->", leet_kw)
        all_params = {}
        for m in method_tag:
            if m == "leetspeak":
                leeter = self.get_random_leetspeak()
                params = leeter.__dict__

                leet_kw = leeter.text2leet(leet_kw)

                # Save arameters
                all_params[m] = params

            if m == "leetspeak-basic":
                leeter = self.get_random_leetspeak(mode="basic")
                params = leeter.__dict__

                leet_kw = leeter.text2leet(leet_kw)

                # Save arameters
                all_params[m] = params

            if m == "leetspeak-covid_basic":
                leeter = self.get_random_leetspeak(mode="covid_basic")
                params = leeter.__dict__

                leet_kw = leeter.text2leet(leet_kw)

                # Save arameters
                all_params[m] = params

            if m == "punct_camo":

                puntc_camo = self.get_random_punt_camo()
                params = puntc_camo.__dict__

                # Other wordcamoufage process can change length of the original kw (Ex. oo --> u)
                # number of injections will be just one in that case
                if len(leet_kw) <= 1:
                    print(f"leet_kw = {leet_kw}, len = {len(leet_kw)}")
                    n_inj = 1
                else:
                    # if kw is long enough just pick a random number of injections
                    n_inj = self.rng.randint(1, len(leet_kw))

                params["n_inj"] = n_inj
                params["text_in"] = leet_kw

                leet_kw = puntc_camo.text2punctcamo(leet_kw, n_inj=n_inj)

                # Save arameters
                params["text_out"] = leet_kw
                all_params[m] = params

            if m == "inv_camo":
                inverter = InversionCamouflage(seed=self.seed)
                params = self.get_params_inverter()
                params["text_in"] = leet_kw
                leet_kw = inverter.text2inversion(
                    leet_kw,
                    lang=params["lang"],
                    max_dist=params["max_dist"],
                    only_max_dist_inv=params["only_max_dist_inv"],
                )

                # Save arameters
                params["text_out"] = leet_kw
                all_params[m] = params

        if len(method_tag) > 1:
            method_tag = "mix"
        else:
            method_tag = method_tag[0]

        return method_tag.upper(), leet_kw, all_params

    def transform(
        self,
        sentence,
        stop_words: Union[List[str], str] = None,
        keyphrase_ngram_range: Tuple[int] = (1, 1),
        important_kws: List[str] = None,
        **kwargs,
    ):
        # print("-"*80)
        # print(sentence)

        NER_data = []
        if not stop_words:
            stop_words = self.lang  # if not stopwords select lang stopwords
        # Compute keyBERT
        kws = self.get_keywords(
            sentence, stop_words, keyphrase_ngram_range, important_kws, **kwargs
        )

        # discard kws with len < 1
        kws = [kw for kw in kws if len(kw) > 1]
        # print("Kws -->", kws)

        ori_data = OrderedDict({"sentence": sentence, "meta": []})
        meta_data = []
        for kw in kws:
            # Get original idxs of keywords
            for m in re.finditer(rf"(?=({kw}\b))", sentence, re.IGNORECASE):
                dict_meta_data = {}
                dict_meta_data["kw"] = kw
                dict_meta_data["init_idxs"] = (m.start(1), m.end(1))
                meta_data.append(dict_meta_data)

        # Sort keywords by occurence
        meta_data = sorted(meta_data, key=lambda i: i["init_idxs"])
        ori_data["meta"].extend(meta_data)

        # Filter overlapping matches. If overlaps get the larger one
        ori_data = self.filter_overlapping(ori_data)

        # Add LeetSpeaker info
        shift = 0
        for dict_in in ori_data["meta"]:
            # Original keyword
            kw_ori = dict_in["kw"]
            ori_idx = dict_in["init_idxs"]

            # Obtain leetspeak version
            # tag, kw_leet, all_params = ToyLeet(kw_ori)
            # apply leetspeak return None if kw_ori len is lower than 1 (min number for n_inj)

            tag, kw_leet, all_params = self.apply_leetspeak(kw_ori)

            # Add LeetSpeaker info
            dict_in["kw_leet"] = kw_leet
            dict_in["params"] = all_params
            if kw_leet != kw_ori:
                dict_in["tag"] = tag
            else:
                dict_in["tag"] = "Unleeted"

            # Calculate the new indexes for each leet_speak keyword
            leet_idxs, shift = self.get_new_idxs(kw_ori, kw_leet, ori_idx, shift)
            dict_in["leet_idxs"] = leet_idxs

        # Obtain leet sentence
        leet_sentence = self.leet_replacement(ori_data)

        return leet_sentence
