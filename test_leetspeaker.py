import unittest
from leetspeaker import LeetSpeaker

class TestRandomChange(unittest.TestCase):
  # Try "random_change" functionality
  
  # Simple example. Only one substitution possible
  def test_RandomChange_one_substitution(self):
    t1 = "a"
    t2 = "#"
    text_in = "We defeated Carlos after party "
    obj = LeetSpeaker(text_in, change_prb=0.8,  change_frq=0.5, mode = "basic", seed = 21, verbose = True)
    res = obj.random_change(t1, t2)
    self.assertEqual(res, "We defeated Carlos #fter p#rty ")

  def test_RandomChangeChangeFrq_one_substitution_change_all(self):
    # Simple example. Only one substitution possible. Change all the matches
    # Testing 'change_frq'
    t1 = "a"
    t2 = "#"
    text_in = "We defeated Carlos after party "    
    obj = LeetSpeaker(text_in, change_prb=0.8,  change_frq=1, mode = "basic", seed = 21)
    res = obj.random_change(t1, t2)
    self.assertEqual(res, "We defe#ted C#rlos #fter p#rty ")

  def test_RandomChangeChangePrb_one_substitution_change_all_no_seed(self):
    # Simple example. Only one substitution possible. Change all the matches
    # Random seed but always do the change. Testing 'change_prb'
    t1 = "a"
    t2 = "#"
    text_in = "We defeated Carlos after party "    
    obj = LeetSpeaker(text_in, change_prb=1,  change_frq=1, mode = "basic", seed = None)
    res = obj.random_change(t1, t2)
    self.assertEqual(res, "We defe#ted C#rlos #fter p#rty "  )

  def test_RandomChange_one_substitution_change_all_longer_than_initial(self):
    # Simple example. Only one substitution possible. Change all the matches
    # Testing if t2 is longer than t1 the substitution is done correctly
    t1 = "a"
    t2 = "$$"
    text_in = "We defeated Carlos after party "    
    obj = LeetSpeaker(text_in, change_prb=0.8,  change_frq=1, mode = "basic", seed = 21)
    res = obj.random_change(t1, t2)
    self.assertEqual(res, "We defe$$ted C$$rlos $$fter p$$rty ")

  def test_RandomChange_several_substitutions(self):
    t1 = "a"
    t2 = ["@", "4", "/\\"]
    text_in = "We defeated Carlos after party "
    obj = LeetSpeaker(text_in, change_prb=0.8,  change_frq=1, mode = "basic", seed = 21)
    res = obj.random_change(t1, t2)
    self.assertEqual(res, "We defe@ted C4rlos /\\fter p@rty ")

class TestText2Leet(unittest.TestCase):
  # def test_Text2Leet_several_substitutions(self):
  #   text_in = "We defeated Carlos after party "
  #   obj = LeetSpeaker(text_in, change_prb=0.8,  change_frq=0.6, mode = "basic", seed = 21, verbose=False)
  #   res = obj.text2leet()
  #   assert res == "We defeated C4rlos @fter p4rty "


  def test_Text2Leet_basic_mode(self):
    text_in = "Pandemia es igual a mentira "
    obj = LeetSpeaker(text_in, change_prb=0.8,  change_frq=0.6, mode = "basic", seed = 30, verbose=False)
    res = obj.text2leet()
    self.assertEqual(res, "P4nd3m1a 3s 1g_4l a mentir4 ")


  def test_Text2Leet_basic_mode_with_accent_end_start_upper_lowercase(self):
    text_in = "A Violación es igual a mentira"
    obj = LeetSpeaker(text_in, change_prb=0.8,  change_frq=1, mode = "basic", seed = 30, verbose=False)
    res = obj.text2leet()
    self.assertEqual(res, "4 Vi0l4ci0n 3s ig_4l 4 m3ntir4")

if "__main__" == __name__:
    unittest.main()
