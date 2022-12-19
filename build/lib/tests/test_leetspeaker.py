# Add the Test Folder path to the sys.path list
from pyleetspeak import (
    LeetSpeaker,
    PunctuationCamouflage,
    InversionCamouflage,
    WordCamouflage_Augmenter,
)
import unittest


class TestText2Leet(unittest.TestCase):
    # def test_Text2Leet_several_substitutions(self):
    #   text_in = "We defeated Carlos after party "
    #   obj = LeetSpeaker(text_in, change_prb=0.8,  change_frq=0.6, mode = "basic", seed = 21, verbose=False)
    #   res = obj.text2leet()
    #   assert res == "We defeated C4rlos @fter p4rty "

    def test_Text2Leet_basic_mode(self):
        text_in = "Pandemia es igual a mentira "
        obj = LeetSpeaker(
            change_prb=0.8, change_frq=0.6, mode="basic", seed=30, verbose=False
        )
        res = obj.text2leet(text_in)
        self.assertEqual(res, "Pand3m1a es ig_4l @ m3nt1r4 ")

    def test_Text2Leet_basic_mode_with_accent_end_start_upper_lowercase(self):
        text_in = "A Violación es igual a mentira"
        obj = LeetSpeaker(
            change_prb=0.8, change_frq=1, mode="basic", seed=30, verbose=False
        )
        res = obj.text2leet(text_in)
        self.assertEqual(res, "@ Viol4cion 3s ig_4l @ m3ntir4")


class TestText2Punct(unittest.TestCase):
    def test_Text2Punct(self):
        text_in = "vacuna"
        wrd_camo = PunctuationCamouflage(
            word_splitting=True, uniform_change=True, seed=21  # for reproducibility
        )

        res = wrd_camo.text2punctcamo(text_in)
        self.assertEqual(res, ".v.a.c.u.n.a")

    def test_Text2Punct_random(self):
        text_in = "vacuna"
        wrd_camo = PunctuationCamouflage(
            word_splitting=False, uniform_change=True, seed=40  # for reproducibility
        )

        res = wrd_camo.text2punctcamo(text_in, n_inj=2)
        self.assertEqual(res, "vac#u#na")

    def test_Text2Punct_custom_symbol(self):
        text_in = "vacuna"
        wrd_camo = PunctuationCamouflage(
            word_splitting=False,
            uniform_change=True,
            punctuation=["~"],
            seed=40,  # for reproducibility
        )
        res = wrd_camo.text2punctcamo(text_in, n_inj=2)
        self.assertEqual(res, "vac~u~na")

    def test_Text2Punct_hyphenization(self):
        text_in = "vacuna"
        wrd_camo = PunctuationCamouflage(
            word_splitting=False,
            uniform_change=True,
            hyphenate=True,
            punctuation=["|"],
            lang="es",
            seed=40,  # for reproducibility
        )
        res = wrd_camo.text2punctcamo(text_in, n_inj=2)
        self.assertEqual(res, "va|cu|na")


class TestText2Inv(unittest.TestCase):
    def test_Text2Inv(self):
        text = "vacuna"
        inverter = InversionCamouflage(seed=21)
        res = inverter.text2inversion(
            text, lang="es", max_dist=1, only_max_dist_inv=True
        )

        self.assertEqual(res, "cuvana")


class TestText2Augmenter(unittest.TestCase):
    def test_Augmenter(self):
        text = "vacuna"
        augmenter = WordCamouflage_Augmenter.augmenter(
            extractor_type="keybert",
            kw_model_name="AIDA-UPM/mstsb-paraphrase-multilingual-mpnet-base-v2",
            max_top_n=5,
            seed=21,
            lang="en",
            # LeetSpeaker parameters
            leet_mode=None,  # Mode of leetspeak. If none, random mode is applied
            leet_change_prb=0.8,
            leet_change_frq=0.5,
            # Probability oof applying uniform change in leetspeak
            leet_uniform_change=0.6,
            # PunctuationCamouflage parameters
            punt_hyphenate_prb=0.5,
            punt_uniform_change_prb=0.6,
            punt_word_splitting_prb=0.5,
            # InversionCamouflage parameters
            inv_max_dist=4,
            inv_only_max_dist_prb=0.5,
            # Probability of applying leetspeak or punct camo. If not, inversion camo is applied
            leet_punt_prb=0.9,
            # Probability of word camouflaging techniques when inversion is not applied
            leet_prb=0.45,
            punct_prb=0.25,
            leet_basic_punt_prb=0.15,
            leet_covid_basic_punt_prb=0.15,
        )
        res = augmenter.transform(text)

        self.assertEqual(res, "vbaqÜπ.")

    def test_Augmenter_only_inversion(self):
        text = "vacuna"
        augmenter = WordCamouflage_Augmenter.augmenter(
            extractor_type="keybert",
            kw_model_name="AIDA-UPM/mstsb-paraphrase-multilingual-mpnet-base-v2",
            max_top_n=5,
            seed=21,
            lang="en",
            # LeetSpeaker parameters
            leet_mode=None,  # Mode of leetspeak. If none, random mode is applied
            leet_change_prb=0.8,
            leet_change_frq=0.5,
            # Probability oof applying uniform change in leetspeak
            leet_uniform_change=0.6,
            # PunctuationCamouflage parameters
            punt_hyphenate_prb=0.5,
            punt_uniform_change_prb=0.6,
            punt_word_splitting_prb=0.5,
            # InversionCamouflage parameters
            inv_max_dist=4,
            inv_only_max_dist_prb=0.5,
            # Probability of applying leetspeak or punct camo. If not, inversion camo is applied
            leet_punt_prb=0.0,  # Only inversion camo is applied
            # Probability of word camouflaging techniques when inversion is not applied
            leet_prb=0.45,
            punct_prb=0.25,
            leet_basic_punt_prb=0.15,
            leet_covid_basic_punt_prb=0.15,
        )
        res = augmenter.transform(text)

        self.assertEqual(res, "cunava")

    def test_Augmenter_yake(self):
        text = "vacuna"
        augmenter = WordCamouflage_Augmenter.augmenter(
            extractor_type="yake",
            max_top_n=5,
            seed=21,
            lang="en",
            # LeetSpeaker parameters
            leet_mode=None,  # Mode of leetspeak. If none, random mode is applied
            leet_change_prb=0.8,
            leet_change_frq=0.5,
            # Probability oof applying uniform change in leetspeak
            leet_uniform_change=0.6,
            # PunctuationCamouflage parameters
            punt_hyphenate_prb=0.5,
            punt_uniform_change_prb=0.6,
            punt_word_splitting_prb=0.5,
            # InversionCamouflage parameters
            inv_max_dist=4,
            inv_only_max_dist_prb=0.5,
            # Probability of applying leetspeak or punct camo. If not, inversion camo is applied
            leet_punt_prb=0.9,  # Only inversion camo is applied
            # Probability of word camouflaging techniques when inversion is not applied
            leet_prb=0.45,
            punct_prb=0.25,
            leet_basic_punt_prb=0.15,
            leet_covid_basic_punt_prb=0.15,
        )
        res = augmenter.transform(text)

        self.assertEqual(res, "vbaqÜπ.")

    def test_Augmenter_yake_sentence(self):
        text = "I am a sentence very long and I want to be leeted"
        augmenter = WordCamouflage_Augmenter.augmenter(
            extractor_type="yake",
            max_top_n=5,
            seed=40,
            lang="en",
            # LeetSpeaker parameters
            leet_mode=None,  # Mode of leetspeak. If none, random mode is applied
            leet_change_prb=0.8,
            leet_change_frq=0.5,
            # Probability oof applying uniform change in leetspeak
            leet_uniform_change=0.6,
            # PunctuationCamouflage parameters
            punt_hyphenate_prb=0.5,
            punt_uniform_change_prb=0.6,
            punt_word_splitting_prb=0.5,
            # InversionCamouflage parameters
            inv_max_dist=4,
            inv_only_max_dist_prb=0.5,
            # Probability of applying leetspeak or punct camo. If not, inversion camo is applied
            leet_punt_prb=0.9,  # Only inversion camo is applied
            # Probability of word camouflaging techniques when inversion is not applied
            leet_prb=0.45,
            punct_prb=0.25,
            leet_basic_punt_prb=0.15,
            leet_covid_basic_punt_prb=0.15,
        )
        res = augmenter.transform(text)

        self.assertEqual(
            res, "I am a 5@n7eπk@ very 10|\|g and I want to be [l{ee.t)e<d"
        )


if "__main__" == __name__:
    unittest.main()
