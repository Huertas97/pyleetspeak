#################################################################################################################################################################################
# Dictionaries for leetspeak substitutions. The target characters are the dictionary keys 
# that will be substituted by the characters of the dictionary values. 
# 
# The possible substitution implemented are divided into different modes depending on the 
# complexity of the resemblance. These substitution have been extracted from different resources:
#
#   - J. Fuchs, “Gamespeak for n00bs - a linguistic and pragmatic analysis of gamers’ language,” Ph.D. dissertation, University of Graz, 2013. [Online]. Available: https://unipub.uni-graz.at/obvugrhs/content/titleinfo/231890?lang=en
#   - K. Blashki and S. Nichol, “Game geek’s goss: linguistic creativity in young males within an online university forum (94/\/\3 933k’5 9055oneone),” 2005
#   - R. Craenen, «Leet speak cheat sheet», GameHouse. https://www.gamehouse.com/blog/leet-speak-cheat-sheet/ (accedido 24 de enero de 2022).
#   - M. Kavanagh, “Bridge the generation gap by decoding leetspeak,” Inside the Internet, vol. 12, no. 12, p. 11, 2005.
#
# COVID-19 leetspeak alphabets has been inspired from:
#   
#   - A. Romero-Vicente, “Word camouflage to evade content moderation,” Dec. 2021. [Online]. Available: https://www.disinfo.eu/publications/word-camouflage-to-evade-content-moderation/
#
#################################################################################################################################################################################


basic_mode = [("a", ["4", "@"]), ("e", ["3"]), ("i", ["1"]), ("o", ["0"]), ("u", ["_"])]



intermediate = [
    ("a", ["4"]),
    ("c", ["["]),
    ("d", ["|)"]),
    ("e", ["3"]),
    ("g", ["6"]),
    ("h", ["#"]),
    ("i", ["1"]),
    ("j", ["]"]),
    ("k", ["|<"]),
    ("l", ["1"]),
    ("m", ["/V\\"]),
    ("n", ["|\\|"]),
    ("o", ["0"]),
    ("p", ["|>"]),
    ("q", ["0_"]),
    ("s", ["5"]),
    ("t", ["7"]),
    ("u", ["_"]),
    ("v", ["\\/"]),
    ("w", ["\\/\\/"]),
    ("x", ["><", "kks"]),
    ("z", ["2"]),
    ("f", ["ph"]),
    ("b", ["|3", "I3"]),
    ("r", ["|2", "I2"]),
    ("y", ["j"]),
]

advanced = [
    ("a", ["4", "@", "/\\"]),
    ("c", ["[", "{", "<"]),
    ("d", [")", "|)", "(|", "[)", "|>"]),
    ("e", ["3", "&", "Ã«"]),
    ("g", ["&", "6", "9", "(_+", "(?,", "[,", "{,"]),
    ("h", ["#", "/-/", "[-]", "]-[", ")-(,", "(-)", ":-:"]),
    ("i", ["1", "[]", "|", "!", "]["]),
    ("j", [",_|", "_|", "._|", "._]", "_]"]),
    ("k", [">|", "|<", "/<", "1<", "|(", "|{"]),
    ("l", ["1", "7", "|_", "|"]),
    ("m", ["/\\/\\", "/V\\", "[V]", "[]V[]", "|\\/|", "^^", "<\\/>", "]\\/["]),
    ("n", ["^/", "|\\|", "/\\/", "[\\]", "<\\>", "{\\}"]),
    ("o", ["(0)", "()", "[]", "<>"]),
    ("p", ["|*", "|Âº", "|^", "|>", "|7"]),
    ("q", ["(_,)", "9", "()_", "2", "0_", "<|", "&"]),
    ("s", ["5", "$", "2"]),
    ("t", ["7", "+", "-|-", "']['", "~|~"]),
    ("v", ["\\/", "|/", "\\|"]),
    ("w", ["\\/\\/", "VV", "\\N", "'//", "\\\\'", "\\^/", "\\|/", "\\_|_/", "\\_:_/"]),
    ("x", ["><", "}{", ")(", "]["]),
    ("z", ["2", "7_", "-/_", "%"]),
    ("f", ["ph", "|=_", "|#", "/="]),
    ("b", ["I3", "8", "13", "|3", "!3", "(3"]),
    ("r", ["I2","2","12","|9","|`","/2"]),
    ("y", ["j","'/'","7","\\|/","\\//"]),
    ("u", ["(_)","|_|","V","L|"])
]



covid_basic_word_camouflage = [
    ("a", ["@", "4", "∆", "*", "", ".", " "]), 
    ("e", ["3", "€", "£", "%",  "@", "*", "", ".", " "]),
    ("i", ["1", "l", "¡", "!", "'", "*", "", ".", " "]),
    ("o", ["0", "ø", "*", "", ".", " "]),
    ("oo", ["u", " "]), 
    ("u", ["_", "Ü", "ü", "*", "" ".", " "]),
]

covid_intermediate_word_camouflage = [
    ("a", ["@", "4", "∆", "*", "", "."]), 
    ("e", ["3", "€", "£", "%",  "@", "*", "", ".",]),
    ("i", ["1", "l", "¡", "!", "'", "*", "", "."]),
    ("o", ["0", "ø", "*", "", "."]),
    ("oo", ["u"]), 
    ("u", ["_", "Ü", "ü", "*", "" "."]),

    ("b", ["ß", "vb", "bv"]),
    ("c", ["q", "k", "©"]),
    ("d", ["t"]),
    ("f", ["ƒ", "ph"]),
    ("h", ["#"]),
    ("k", ["₭"]),
    ("l", ["1", "ʅ"]), 
    ("m", ["ʍ"]),
    ("n", ["π", "¬"]),
    ("p", ["₱"]),
    ("r", ["₹"]), 
    ("s", ["5", "$", "z"]),
    ("t", ["7", "Ŧ"]),
    ("v", ["b", "vb", "bv", "\\/", "▼"]),
    ("w", ["ω"]),
    ("x", ["><", "kks", "×"]),
    ("y", ["¥"]),
    ("z", ["ẕ"]),
]
