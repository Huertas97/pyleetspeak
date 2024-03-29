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
    ("n", ["|\\|", "/\\/", "[\\]", "{\\}"]), # "^/", "<\\>",
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



##### AUGMENTER MODES

# It is pretty readable and understandable
# 1. simple character substitution. 
# 2. substituting every vowel for a number. 
basic_leetspeak = [
    ("a", ['4', '@', 'ä', 'ā', 'ă', 'ą', "Ƌ", "ȁ", "Ʌ", "ȃ", "ǻ", "Д", "∆", "∀", "α", "ⱥ"]), 
    ('e', ['3', 'ë', '€', 'ē', 'ĕ', 'ė', 'ę', 'ě', "Œ", "œ", "℮", "₤", "Æ", "Ə", "Ɛ", "Ƹ", "ƹ", "ȇ", "ꬲ", "ͼ"]), 
    ("i", ['1', '!', '¡', 'ï', "ĩ", "ĭ", "į", "ı", "í"]),
    ("o", ['0', '<>', 'Ø', 'ö', "ō", "ŏ", "ő", "Ɵ", "ȯ", "ȱ", "ʘ", "Θ", "ꬽ"]), 
    ("u", ["_", 'ü', "ũ", "ū", "Ŭ", "ŭ", "ų", "Ʊ", "บ"])
]

# Readability and understandable is harder. 
# 1. Latin alphabet extended and complex character substitution, punctuation injection, and simple word inversions. 
# 2. Vowel substitution
# 3. Consonants are also substituted.
# 4. These characters are substituted with either numbers or simple punctuation marks in a reduced number of ways. 
# 5. Readable symbols from other alphabets that closely resemble the regular alphabet characters are included. 
intermediate_leetspeak = [
     ('a', ['4', '@', 'ä', 'ā', 'ă', 'ą', "Ƌ", "ȁ", "Ʌ", "ȃ", "ǻ"]),
     ('b', ['|3', 'I3', 'ß', "₿", "฿", "ƅ", "Ƅ", "ƀ"]),
     ('c', ['[', '©', '{', 'ç', 'ć', 'ĉ', 'ċ', 'č', '¢']),
     ('d', ['|)', 'Ď', 'ď', 'Đ', 'đ']),
     ('e', ['3', 'ë', '€', 'ē', 'ĕ', 'ė', 'ę', 'ě', "œ", "℮", "₤", "Æ", "Ə", "Ɛ", "Ƹ", "ƹ", "ȇ", "ꬲ", "ͼ"]), #"Œ"
     ('f', ['ƒ', 'ℱ', "ſ", "₣", "ϝ"]),
     ('g', ['6', '9', 'ĝ', 'ğ', 'ġ', 'ģ']),
     ('h', ['#', '|-|', '|+|', 'ĥ', 'ħ']),
     ('i', ['1', '!', '¡', 'ï', "ĩ", "ĭ", "į", "ı"]),
     ('j', [']', '._|', "Ĳ", "ĳ", "Ĵ", "ĵ", "⌡"]),
     ('k', ['|<', '!<', '𝕂', "Ķ", 'ķ', "ĸ"]),
     ('l', ['1', '|_', '|', '£', 'ℒ', 'ł', "ĺ", "ļ", "ľ", "ŀ", "ł", "ℓ", "∟"]),
     ('m', ['/V\\', '[V]', ']V[', 'ʍ', 'ℳ', "ɅɅ", "ɱ"]),
     ('n', ['|\\|', '{\\}', 'ñ', 'ℕ', 'η', "ń", "ņ", "ň", "ŋ", "ŉ", "₦", "ͷ"]),     
     ('o', ['0', '<>', 'Ø', 'ö', "ō", "ŏ", "ő", "Ɵ", "ȯ", "ȱ", "ʘ", "Θ", "ꬽ"]),
     ('p', ['|>', '₱', 'ℙ']),
     ('q', ['0_', '9', '()_']),
     ('r', ['/2', 'Я', '®', 'ℝ', "ŕ", "ŗ", "ř"]),
     ('s', ['5', '§', '$', "ś", "ŝ", "ş", "š", "ϟ"]),
     ('t', ['7', '+', "Ţ", "ţ", "ť",  "ŧ", "ţ", "†", "₸", "ₜ", "ᵗ", "ͳ", "†", "Ⴕ", "ȶ", "ǂ"]),
     ('u', ['|_|', '(_)', 'ü', "ũ", "ū", "Ŭ", "ŭ", "ų", "Ʊ"]),
     ('v', ['\\/', "ṽ", "ṿ", "۷", "ᵛ"]),
     ('w', ['\\/\\/', 'ω', "ŵ"]),
     ('x', ['><', '}{', "ꭙ"]),
     ('y', ['¥', "'/'", 'γ', "Ų", "ŷ", "ÿ", "ɏ", "ϒ", "ʸ", "ꭚ"]),
     ('z', ['2', '%', 'ž', '𝕫', 'ℤ', "ź", "ż"])
]


# Readability and understandable is a challenge.
# Advanced Leet is in fact a combination of Basic and Intermediate Leet, but increases the use of punctuation marks 
# 1. Intermediate techniques as well as more complex word inversions and character substitution. 
# 2. Vowel and Consonants are substituted.
# 3. These characters are replaced by numbers and various punctuation symbols. The punctuation symbols considered are larger and more complex.
# 4. The number of readable symbols from other alphabets that closely resemble the regular alphabet characters increase and are more complex.
# 5. Mathematical symbols are included
advanced_leetspeak = [
     ('a', ['4', '@', 'ä', 'ā', 'ă', 'ą', "Ƌ", "ȁ", "Ʌ", "ȃ", "ǻ", "/\\", "Д", "∆", "∀", "α", "ⱥ", "Â", "Ã"]),
     ('b', ['|3', 'I3', 'ß', "₿", "฿", "ƅ", "Ƅ", "ƀ", "8", "13", "!3", ]), # "(3", "j3"
     ('c', ['[', '©', '{', 'ç', 'ć', 'ĉ', 'ċ', 'č', '¢', "<", "ç", "ℂ", "«", "ↄ"]),
     ('d', ['|)', 'Ď', 'ď', 'Đ', 'đ', ")", "(|", "[)", "|>", "∂"]),
     ('e', ['3', 'ë', '€', 'ē', 'ĕ', 'ė', 'ę', 'ě', "œ", "℮", "₤", "Æ", "Ə", "Ɛ", "Ƹ", "ƹ", "ȇ", "ꬲ", "ͼ", "∈", "ℯ", "∃", "Σ", "[-"]), # "Œ"
     ('f', ['ƒ', 'ℱ', "ſ", "₣", "ϝ", "ph", "|=_", "|#", "/="]),
     ('g', ['6', '9', 'ĝ', 'ğ', 'ġ', 'ģ', "(_+", "(?,", "[,", "{,", "(+", "¶", "gee"]),
     ('h', ['#', '|-|', '|+|', 'ĥ', 'ħ', "/-/", "[-]", "]-[", ")-(", "(-)", ":-:", ")-(,", "ℋ", "ⱨ"]),
     ('i', ['1', '!', '¡', 'ï', "ĩ", "ĭ", "į", "ı", "|", "][", "í"]),
     ('j', [']', '._|', "Ĳ", "ĳ", "Ĵ", "ĵ", "⌡", ",_|", "_|", "._]", "_]", ",|", "|", ".|", ".]"]),
     ('k', ['|<', '!<', '𝕂', "Ķ", 'ķ', "ĸ", ">|", "/<", "1<", "|(", "|{", "₭", "ⱪ"]),
     ('l', ['1', '|_', '|', '£', 'ℒ', 'ł', "ĺ", "ļ", "ľ", "ŀ", "ł", "ℓ", "∟", "ʅ"]),
     ('m', ['/V\\', '[V]', ']V[', 'ʍ', 'ℳ', "ɅɅ", "ɱ", "/\\/\\", "[]V[]", "|\\/|", "^^", "]\\/[", "₼", "µ", "₥"]), # , "<\\/>" , "</>", "]/[",
     ('n', ['|\\|', '{\\}', 'ñ', 'ℕ', 'η', "ń", "ņ", "ň", "ŋ", "ŉ", "₦", "ͷ",  "/\\/", "[\\]",  "ท", "π",  "η"]), # "<\\>", "^/", "¬",
     ('o', ['0', '<>', 'Ø', 'ö', "ō", "ŏ", "ő", "Ɵ", "ȯ", "ȱ", "ʘ", "Θ", "ꬽ", "º", "(0)", "()", "[]", "φ", "Ω", "¤", "●", "○"]),
     ('p', ['|>', '₱', 'ℙ', "|>", "|*", "[]D", "|^",  "|#", "₱", "|^",  "þ"]), # "|Âº", "|7", "|7",
     ('q', ['0_', '9', '()_', "(_,)", "<|", "&"]),
     ('r', ['/2', 'Я', '®', 'ℝ', "ŕ", "ŗ", "ř", "2", "12","|9","|`", "₹", "𝔑", "Ɽ"]),
     ('s', ['5', '§', '$', "ś", "ŝ", "ş", "š", "ϟ", "∫"]),
     ('t', ['7', '+', "Ţ", "ţ", "ť",  "ŧ", "ţ", "†", "₸", "ₜ", "ᵗ", "ͳ", "†", "Ⴕ", "ȶ", "ǂ", "-|-", "']['", "~|~", "Ŧ", "⊥"]),
     ('u', ['|_|', '(_)', 'ü', "ũ", "ū", "Ŭ", "ŭ", "ų", "Ʊ", "L|", "บ", "└┘", "µ", "ʊ"]),
     ('v', ['\\/', "ṽ", "ṿ", "۷", "ᵛ", "|/", "\\|", "▼", "√"]),
     ('w', ['\\/\\/', 'ω', "ŵ", "VV",  "\\^/", "\\_|_/", "\\_:_/", "Ш", "Щ", "พ", "ѡ", "𝕎", "₩", "v²"]), # "\\N", "'//", "\\\\'",  "\\|/"
     ('x', ['><', '}{', "ꭙ", ")(", "][", "×", "χ"]),
     ('y', ['¥', "'/'", 'γ', "Ų", "ŷ", "ÿ", "ɏ", "ý", "ÿ", "ϒ", "ʸ", "ꭚ", "7","\\|/", "Ч"]), # "\\//",
     ('z', ['2', '%', 'ž', '𝕫', 'ℤ', "ź", "ż", "7_",  "ẕ", "ζ"]) # "-/_",
]



# [
#      ('a', ['4', '@', 'ä', 'ā', 'ă', 'ą', "Ƌ", "ȁ", "Ʌ", "ȃ", "ǻ", "/\\", "Д", "∆", "∀", "α", "ⱥ"]),
#      ('b', ['|3', 'I3', 'ß', "₿", "฿", "ƅ", "Ƅ", "ƀ", "8", "13", "!3", "(3"]),
#      ('c', ['[', '©', '{', 'ç', 'ć', 'ĉ', 'ċ', 'č', '¢', "<", "ç", "ℂ", "«", "ↄ"]),
#      ('d', ['|)', 'Ď', 'ď', 'Đ', 'đ', ")", "(|", "[)", "|>", "∂"]),
#      ('e', ['3', 'ë', '€', 'ē', 'ĕ', 'ė', 'ę', 'ě', "Œ", "œ", "℮", "₤", "Æ", "Ə", "Ɛ", "Ƹ", "ƹ", "ȇ", "ꬲ", "ͼ", "∈", "ℯ", "∃", "Σ", "[-"]),
#      ('f', ['ƒ', 'ℱ', "ſ", "₣", "ϝ", "ph", "|=_", "|#", "/="]),
#      ('g', ['6', '9', 'ĝ', 'ğ', 'ġ', 'ģ', "(_+", "(?,", "[,", "{,"]),
#      ('h', ['#', '|-|', '|+|', 'ĥ', 'ħ', "/-/", "[-]", "]-[", ")-(", "ℋ", "ⱨ"]),
#      ('i', ['1', '!', '¡', 'ï', "ĩ", "ĭ", "į", "ı", "|", "][", "í"]),
#      ('j', [']', '._|', "Ĳ", "ĳ", "Ĵ", "ĵ", "⌡", ",_|", "_|", "._]", "_]"]),
#      ('k', ['|<', '!<', '𝕂', "Ķ", 'ķ', "ĸ", ">|", "/<", "1<", "|(", "|{", "₭", "ⱪ"]),
#      ('l', ['1', '|_', '|', '£', 'ℒ', 'ł', "ĺ", "ļ", "ľ", "ŀ", "ł", "ℓ", "∟", "ʅ"]),
#      ('m', ['/V\\', '[V]', ']V[', 'ʍ', 'ℳ', "ɅɅ", "ɱ", "/\\/\\", "[]V[]", "|\\/|", "^^", "<\\/>", "]\\/[", "₼"]),
#      ('n', ['|\\|', '{\\}', 'ñ', 'ℕ', 'η', "ń", "ņ", "ň", "ŋ", "ŉ", "₦", "ͷ", "^/", "/\\/", "[\\]", "<\\>", "ท", "π", "¬", "η"]),     
#      ('o', ['0', '<>', 'Ø', 'ö', "ō", "ŏ", "ő", "Ɵ", "ȯ", "ȱ", "ʘ", "Θ", "ꬽ", "º", "(0)", "()", "[]", "φ", "Ω", "¤", "●", "○"]),
#      ('p', ['|>', '₱', 'ℙ', "|>", "|*", "[]D", "|^", "|7", "|#", "₱"]),
#      ('q', ['0_', '9', '()_', "(_,)", "<|", "&"]),
#      ('r', ['/2', 'Я', '®', 'ℝ', "ŕ", "ŗ", "ř", "2", "12","|9","|`", "₹", "𝔑", "Ɽ"]),
#      ('s', ['5', '§', '$', "ś", "ŝ", "ş", "š", "ϟ", "∫"]),
#      ('t', ['7', '+', "Ţ", "ţ", "ť",  "ŧ", "ţ", "†", "₸", "ₜ", "ᵗ", "ͳ", "†", "Ⴕ", "ȶ", "ǂ", "-|-", "']['", "~|~", "Ŧ", "⊥"]),
#      ('u', ['|_|', '(_)', 'ü', "ũ", "ū", "Ŭ", "ŭ", "ų", "Ʊ", "L|", "บ", "└┘"]),
#      ('v', ['\\/', "ṽ", "ṿ", "۷", "ᵛ", "|/", "\\|", "▼", "√"]),
#      ('w', ['\\/\\/', 'ω', "ŵ", "VV", "\\N", "'//", "\\\\'", "\\^/", "\\|/", "\\_|_/", "\\_:_/", "Ш", "Щ", "พ"]),
#      ('x', ['><', '}{', "ꭙ", ")(", "][", "×"]),
#      ('y', ['¥', "'/'", 'γ', "Ų", "ŷ", "ÿ", "ɏ", "ϒ", "ʸ", "ꭚ", "7","\\|/","\\//", "Ч"]),
#      ('z', ['2', '%', 'ž', '𝕫', 'ℤ', "ź", "ż", "7_", "-/_"])
# ]

# Readability and understandable is a challenge.
# Vowels and consonants can be substituted by various complex
# punctuation symbols, letters from other alphabets that reseemble, 
# mathematic symbols
# makes harder the readabilty
# We include pronunciation substitutions "kks" "ecks" -> x "ph" -> f  "j" -> y  m -> "nn"  u -> "oo", o -> "oh", s -> "ehs" b -> "v" g --> "gee"
expert_leetspeak = [
     ('a', ['4', '@', 'ä', 'ā', 'ă', 'ą', "Ƌ", "ȁ", "Ʌ", "ȃ", "ǻ", "/\\", "Д", "∆", "∀", "α", "ⱥ", "Â", "Ã"]),
     ('b', ['|3', 'I3', 'ß', "₿", "฿", "ƅ", "Ƅ", "ƀ", "8", "13", "!3", "(3", "j3"]),
     ('c', ['[', '©', '{', 'ç', 'ć', 'ĉ', 'ċ', 'č', '¢', "<", "ç", "ℂ", "«", "ↄ"]),
     ('d', ['|)', 'Ď', 'ď', 'Đ', 'đ', ")", "(|", "[)", "|>", "∂"]),
     ('e', ['3', 'ë', '€', 'ē', 'ĕ', 'ė', 'ę', 'ě', "Œ", "œ", "℮", "₤", "Æ", "Ə", "Ɛ", "Ƹ", "ƹ", "ȇ", "ꬲ", "ͼ", "∈", "ℯ", "∃", "Σ", "[-"]),
     ('f', ['ƒ', 'ℱ', "ſ", "₣", "ϝ", "ph", "|=_", "|#", "/="]),
     ('g', ['6', '9', 'ĝ', 'ğ', 'ġ', 'ģ', "(_+", "(?,", "[,", "{,", "(+", "¶", "gee"]),
     ('h', ['#', '|-|', '|+|', 'ĥ', 'ħ', "/-/", "[-]", "]-[", ")-(", "(-)", ":-:", ")-(,", "ℋ", "ⱨ"]),
     ('i', ['1', '!', '¡', 'ï', "ĩ", "ĭ", "į", "ı", "|", "][", "í"]),
     ('j', [']', '._|', "Ĳ", "ĳ", "Ĵ", "ĵ", "⌡", ",_|", "_|", "._]", "_]", ",|", "|", ".|", ".]"]),
     ('k', ['|<', '!<', '𝕂', "Ķ", 'ķ', "ĸ", ">|", "/<", "1<", "|(", "|{", "₭", "ⱪ"]),
     ('l', ['1', '|_', '|', '£', 'ℒ', 'ł', "ĺ", "ļ", "ľ", "ŀ", "ł", "ℓ", "∟", "ʅ"]),
     ('m', ['/V\\', '[V]', ']V[', 'ʍ', 'ℳ', "ɅɅ", "ɱ", "/\\/\\", "[]V[]", "|\\/|", "^^", "<\\/>", "]\\/[", "₼", "</>", "]/[", "µ", "₥"]),
     ('n', ['|\\|', '{\\}', 'ñ', 'ℕ', 'η', "ń", "ņ", "ň", "ŋ", "ŉ", "₦", "ͷ", "^/", "/\\/", "[\\]", "<\\>", "ท", "π", "¬", "η"]),     
     ('o', ['0', '<>', 'Ø', 'ö', "ō", "ŏ", "ő", "Ɵ", "ȯ", "ȱ", "ʘ", "Θ", "ꬽ", "º", "(0)", "()", "[]", "φ", "Ω", "¤", "●", "○"]),
     ('p', ['|>', '₱', 'ℙ', "|>", "|*", "[]D", "|^", "|7", "|#", "₱", "|Âº", "|^", "|7", "þ"]),
     ('q', ['0_', '9', '()_', "(_,)", "<|", "&"]),
     ('r', ['/2', 'Я', '®', 'ℝ', "ŕ", "ŗ", "ř", "2", "12","|9","|`", "₹", "𝔑", "Ɽ"]),
     ('s', ['5', '§', '$', "ś", "ŝ", "ş", "š", "ϟ", "∫"]),
     ('t', ['7', '+', "Ţ", "ţ", "ť",  "ŧ", "ţ", "†", "₸", "ₜ", "ᵗ", "ͳ", "†", "Ⴕ", "ȶ", "ǂ", "-|-", "']['", "~|~", "Ŧ", "⊥"]),
     ('u', ['|_|', '(_)', 'ü', "ũ", "ū", "Ŭ", "ŭ", "ų", "Ʊ", "L|", "บ", "└┘", "µ", "ʊ"]),
     ('v', ['\\/', "ṽ", "ṿ", "۷", "ᵛ", "|/", "\\|", "▼", "√"]),
     ('w', ['\\/\\/', 'ω', "ŵ", "VV", "\\N", "'//", "\\\\'", "\\^/", "\\|/", "\\_|_/", "\\_:_/", "Ш", "Щ", "พ", "ѡ", "𝕎", "₩", "v²"]),
     ('x', ['><', '}{', "ꭙ", ")(", "][", "×", "χ"]),
     ('y', ['¥', "'/'", 'γ', "Ų", "ŷ", "ÿ", "ɏ", "ý", "ÿ", "ϒ", "ʸ", "ꭚ", "7","\\|/","\\//", "Ч"]),
     ('z', ['2', '%', 'ž', '𝕫', 'ℤ', "ź", "ż", "7_", "-/_", "ẕ", "ζ"])
]


