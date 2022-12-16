# Add the Test Folder path to the sys.path list
from pyleetspeak import LeetSpeaker, PunctuationCamouflage
import unittest


class TestText2Leet(unittest.TestCase):
    # def test_Text2Leet_several_substitutions(self):
    #   text_in = "We defeated Carlos after party "
    #   obj = LeetSpeaker(text_in, change_prb=0.8,  change_frq=0.6, mode = "basic", seed = 21, verbose=False)
    #   res = obj.text2leet()
    #   assert res == "We defeated C4rlos @fter p4rty "

    def test_Text2Leet_basic_mode(self):
        text_in = "Pandemia es igual a mentira "
        obj = LeetSpeaker(change_prb=0.8,  change_frq=0.6,
                          mode="basic", seed=30, verbose=False)
        res = obj.text2leet(text_in)
        self.assertEqual(res, "Pand3m1a es ig_4l @ m3nt1r4 ")

    def test_Text2Leet_basic_mode_with_accent_end_start_upper_lowercase(self):
        text_in = "A Violación es igual a mentira"
        obj = LeetSpeaker(change_prb=0.8,  change_frq=1,
                          mode="basic", seed=30, verbose=False)
        res = obj.text2leet(text_in)
        self.assertEqual(res, "@ Viol4cion 3s ig_4l @ m3ntir4")


class TestText2Punct(unittest.TestCase):

    def test_Text2Punct(self):
        text_in = "vacuna"
        wrd_camo = PunctuationCamouflage(
            word_splitting=True,
            uniform_change=True,
            seed=21  # for reproducibility
        )

        res = wrd_camo.text2punctcamo(text_in)
        self.assertEqual(res, '.v.a.c.u.n.a')

    def test_Text2Punct_random(self):
        text_in = "vacuna"
        wrd_camo = PunctuationCamouflage(
            word_splitting=False,
            uniform_change=True,
            seed=40  # for reproducibility
        )

        res = wrd_camo.text2punctcamo(text_in, n_inj=2)
        self.assertEqual(res, 'vac#u#na')

    def test_Text2Punct_custom_symbol(self):
        text_in = "vacuna"
        wrd_camo = PunctuationCamouflage(
            word_splitting=False,
            uniform_change=True,
            punctuation=["~"],
            seed=40  # for reproducibility
        )
        res = wrd_camo.text2punctcamo(text_in, n_inj=2)
        self.assertEqual(res, 'vac~u~na')


if "__main__" == __name__:
    unittest.main()
