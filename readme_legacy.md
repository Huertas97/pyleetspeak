# LeetTransformer :one::three::three::seven::robot:


  - [Overview](#overview)
  - [Installation](#installation)
  - [**Word camouflaging**](#word-camouflaging)
    - [**LeetSpeaker**](#leetspeaker)
      - [Parameters](#parameters)
      - [Modes](#modes)
      - [Basic Use](#basic-use)
      - [Define your own changes](#define-your-own-changes)
      - [Uniform substitutions](#uniform-substitutions)
      - [Get all changes](#get-all-changes)
    - [**PuntctuationCamouflage**](#puntctuationcamouflage)
      - [Parameters](#parameters-1)
      - [Basic Use](#basic-use-1)
      - [Uniform punctuation injections](#uniform-punctuation-injections)
      - [User-defined character injections](#user-defined-character-injections)
      - [Hyphenitation](#hyphenitation)
    - [**InversionCamouflage**](#inversioncamouflage)
      - [Parameters](#parameters-2)
      - [Basic Use](#basic-use-2)

  - [**Leet NER data Generator**](#leet-ner-data-generator)
      - [Usage](#usage)
      - [NER data formats](#ner-data-formats)


## Overview

---

Word camouflage is currently used to evade content moderation in Social Media. Therefore, this tool aims to counter new misinformation that emerges in social media platforms by providing a mechanism for simulating and generating leetspeak/word camouflaging data. 


`pyleetspeak` includes three different, but compatible, text modifications word camouflaging methods: `LeetSpeaker`, `PuntctuationCamouflage` and `InversionCamouflage`.

- `LeetSpeaker`: This module apply the canonical 'leetspeak' method of producing visually similar character strings by replacing alphabet characters with special symbols or numbers. There's many different ways you can use leet speak. Ranging from basic vowel substitutions to really advanced combinations of various punctuation marks and glyphs. Different leetspeak levels are included.
- `PuntctuationCamouflage`: This module apply punctuation symbol injections in the text. It is another version of producing visually similar character strings. The location of the punctuation injections and the symbols used can be selected by the user. 
- `InversionCamouflage`: This module create new camouflaged version of words by inverting the order of the syllables. It works by separating a input text in syllabels, select two syllabels and invert them.

These modules can be combined into a string to generate a leetspeak version of an input text. Precisely, this can be achieved by using the `Leet_NER_generator` method that selects the most semantically relevant words from an input text, applies word camouflage and creates compatible annotations for NER detection.

## Installation

---

````bash
pip install pyleetspeak
````

## **Word camouflaging**

---

### **LeetSpeaker**

Canonical [leetspeak](https://en.wikipedia.org/wiki/Leet) in which standard letters are often replaced by numerals or special characters that resemble the letters in appearance

---

#### **Parameters**


You can see an example of use in a Heroku App:

<https://user-images.githubusercontent.com/56938752/147962824-c347e184-14b6-41fe-8b05-ef670ac0a5f9.mp4>

The only required argument that the user has to provide is the `text_in` argument which represent the casual text to transform to leetspeak. Nonetheless, there are other optional arguments that control the behaviour of the transformation:`

- `change_prb` determines the probability of a transformation to take place (i.e, if it is equal 1 all the possible transformation will be applied).
- `change_frq` is affects how frequently a transformation will occur (i.e, if it is equal 1 all the letters of this transformation type will be changed).
- `mode` controls the level of leetspeak transformation. Currently only `basic` mode is available. We are working on more modes. Stay tuned.
- `seed` controls the reproducibility of the results. By default no seed is applied.
- `verbose` controls the verbosity of the proccess.
- `get_all_combs` to obtain all the possible leetspeak versions of a casual text
- `uniform_change` determines if the same substitution character should be used in all the positions where the casual text will be modified.

Minor concerns about the package behaviour: accents are deleted using `Unidecode`. This is important for languages like Spanish, where the word "melocotón" is preprocessed as "melocoton" and finally transformed to leetspeak.

---


#### **Modes**


There are several modes available:

- `basic`
- `intermediate`
- `advanced`
- `covid_basic`
- `covid_intermediate`

---

#### **Basic Use**

Let's see a simple working example:

````python
from pyleetspeak import LeetSpeaker

text_in = "I speak leetspeak"
leeter = LeetSpeaker(
    change_prb=0.8, change_frq=0.6, mode="basic", seed=None, verbose=False
)
leet_result = leeter.text2leet(text_in)
print(leet_result)
````

For the sake of reproducibility you can set a random seed:

````python
from pyleetspeak import LeetSpeaker

leeter = LeetSpeaker(
    change_prb=0.8,
    change_frq=0.5,
    mode="basic",
    seed=42,  # for reproducibility purposes
    verbose=False,
)
leet_result = leeter.text2leet(text_in)
print(leet_result)
# "1 sp34k leetsp3ak"
````
---

#### **Define your own changes**

`pyleetspeak` is prepared to apply substitutions defined by the user. It is essential to highlight that these new user-defined changes have to follow two possible formats, dictionary or List of tuples. Here we show a toy example to add two new target characters from the original text to be replaced by two and one different characters, respectively:

- Dictionary type:

  ````python
  {"target_chr_1": ["sub_chr_1", "sub_chr_1"], "target_chr_2": ["sub_chr_1"]}
  ````

- List[Tuple] type:
  
  ````python
  [("target_chr_1", ["sub_chr_1", "sub_chr_1"]), (("target_chr_2", ["sub_chr_1"])]
  ````

You can add new user-defined substitutions:

````python
from pyleetspeak import LeetSpeaker

text_in = "New changes Leetspeak"
letter = LeetSpeaker(
    change_prb=1,
    change_frq=0.8,
    mode="basic",
    seed=21,
    verbose=False,
    get_all_combs=False,
    user_changes=[("a", "#"), ("s", "$")],  # user-defined changes
)
print(letter.text2leet(text_in))
# N3w ch@ng3$ L33t$pe4k
````

Moreover, you can use only the user-defined substitutions:

````python
from pyleetspeak import LeetSpeaker

text_in = "Only user changes: Leetspeak"
letter = LeetSpeaker(
    change_prb=1,
    change_frq=0.8,
    mode=None, # None pre-defined changes will be applied
    seed=21,
    verbose=False,
    get_all_combs=False,
    user_changes = [("a", "#"), ("s", "$")], # user-defined changes
)
print(letter.text2leet(text_in))
# Only u$er ch#nge$: Leet$pe#k
````
---

#### **Uniform substitutions**

Usually, the same substitution character is used in all the matches for a specific substitution type. In other words, the same target character is usually replaced by the same substitution character. In order to reproduce this situation, `pyleetspeak` includes the `uniform_change` parameter that determines if all the matches of a target character are jointly or independently substituted. In the following example notice how the target character "e" is always replaced by "€" when `uniform_changes` is se to `True`.

````python
from pyleetspeak import LeetSpeaker

text_in = "Leetspeak"
leeter = LeetSpeaker(
    change_prb=1,  # All subs type will occur
    change_frq=1,  # All matches of target chr will be changed
    mode="basic",
    seed=41,
    user_changes=[
        ("e", ["3", "%", "€", "£"])
    ],  # Add diferent subs characters for target chr "e"
    uniform_change=True,  # Use the same substitution chr for each target chr
)
print(leeter.text2leet(text_in))
# L€€tsp€4k
````

---

#### **Get all changes**

You can also obtain all the possible versions of a leetspeak text using the `get_all_combs` parameter like this:

````python
from pyleetspeak import LeetSpeaker

text_in = "leetspeak"
leeter = LeetSpeaker(
    mode="basic",
    get_all_combs=True,
    user_changes = [("e", "€"), ("s", "$")], # user-defined changes
)
leet_result = leeter.text2leet(text_in)
print(len(leet_result))
assert len(leet_result) == 162 # all possible combinations
leet_result[20]
# 162
# 'le3t$p34k'
````

If you are only interested in the combinations that apply the same substitution character for each target target, you can also set `uniform_change` to `True`.

````python
from pyleetspeak import LeetSpeaker

text_in = "leetspeak"
leeter = LeetSpeaker(
    mode="basic",
    get_all_combs=True,
    user_changes = [("e", "€"), ("s", "$")], # user-defined changes
    uniform_change = True
)
leet_result = leeter.text2leet(text_in)
print(len(leet_result))
assert len(leet_result) == 90 # all possible combinations
leet_result[60]
# 90
# 'le3t$peak'
````

---

### **PuntctuationCamouflage**

Word camouflge using punctuation injections

---

#### **Parameters**

- ``seed`` (int, optional): Seed for reproducible results. Defaults to None.
- ``uniform_change`` (bool, optional): Determines if the same punctuation character should be used in all the position where punctuation is injected . Defaults to False.
- ``hyphenate`` (bool, optional): Determines if the punctuation symbols should be injected in syllables or hyphenate locations. Defaults to False.
- ``word_splitting`` (bool, optional): Determines if the puntuation symbols should be injected in all the possible positions. The final output depends also if `hypenate` or `uniform_change` are selected. Defaults to False.
- ``punctuation`` (List[str], optional): List of puntuation symbols to use for the camouflage injection. Defaults to string.punctuation+" ".
- ``lang`` (str, optional): Language to be used in the `hyphenate` process. Defaults to "es".

---

#### **Basic Use**

Another method of producing visually similar character strings is to inject punctuation symbols. `pyleetspeak` includes another functionality named `PunctuationCamouflage` that takles this situation.

Let's see an example where we create a punctuation injected version of the spanish word `vacuna` (vaccine in English).

````python
from pyleetspeak import PuntctuationCamouflage

text_in = "vacuna"
wrd_camo = PuntctuationCamouflage(seed=21)  # for reproducibility
wrd_camo.text2punctcamo(text_in, n_inj=2)
# 'v_ac=una'
````

You can also specify the behaviour of the punctuation injection. 

Let's get different punctuation symbols between all the letters in the spanish word `vacuna` with `word_splitting` set to `True`.

````python
from pyleetspeak import PuntctuationCamouflage

wrd_camo = PuntctuationCamouflage(
    word_splitting=True,
    seed=21
)

wrd_camo.text2punctcamo("vacuna")
# '|v.a;c}u^n&a'

````

---

#### **Uniform punctuation injections**

The same process but now using the same punctuation symbol using `uniform_change`.

````python
from pyleetspeak import PuntctuationCamouflage

wrd_camo = PuntctuationCamouflage(
    word_splitting=True,
    uniform_change=True,
    seed=21 # for reproducibility
)

wrd_camo.text2punctcamo("vacuna")
# '.v.a.c.u.n.a'
````

We can also inject puntuation symbols in random positions. Let's inject the same puntuation symbol 2 times.

````python
from pyWordCamouflage import PuntctuationCamouflage

wrd_camo = PuntctuationCamouflage(
    word_splitting=False, uniform_change=True, seed=40  # for reproducibility
)

wrd_camo.text2punctcamo("vacuna", n_inj=2)
# 'vac#u#na'
````

---

#### **User-defined character injections**

By default the punctuation symbols used are the one from `string.punctuation` built-in Python module. You can establish which punctuation symbols should be used.

````python
from pyleetspeak import PuntctuationCamouflage

wrd_camo = PuntctuationCamouflage(
    word_splitting=False,
    uniform_change=True,
    punctuation = ["~"], 
    seed=40 # for reproducibility
)

wrd_camo.text2punctcamo("vacuna", n_inj=2)
# 'vac~u~na'
````

---

#### **Hyphenitation**

Usually the punctuation symbol injections occur between syllables. `PunctuationCamouflage` can lead with this situation using hyphenation dictionaries from `pyphen` PyPi Package. Hypenation dictionaries have language dependent rules for setting boundaries for hyphen. Thus, `lang` should be passed for a right syllabels detection. Currently, 69 languages are supported. To enable this kind of punctuation injection set `hyphenate` to `True`.

````python
from pyleetspeak import PuntctuationCamouflage

wrd_camo = PuntctuationCamouflage(
    word_splitting=False,
    uniform_change=True,
    hyphenate=True,
    punctuation = ["|"], 
    lang="es",
    seed=40 # for reproducibility
)

wrd_camo.text2punctcamo("vacuna", n_inj=2)
# 'va|cu|na'
````

Notice the importance of `lang` for the syllabels detection. Instead of Spanish we will use Englisg hyphenate dictionaries. English will only detect one syllables boundary ("va-cuna") instead of two ("va-cu-na"). Notice also that a `RunTimeWarning` has been raised informing that we hace specified more punctuation injections (`n_inj`=2) than syllables boundaries available.

````python
from pyleetspeak import PuntctuationCamouflage

wrd_camo = PuntctuationCamouflage(
    word_splitting=False,
    uniform_change=True,
    hyphenate=True,
    punctuation = ["|"], 
    lang="en",
    # seed=40 # for reproducibility
)

wrd_camo.text2punctcamo("vacuna", n_inj=2)
# RuntimeWarning: You have selected `hyphenate` = True with a number of punctuation marks to insert (2) greater than the maximum number of positions to hyphenate (1). Therefore, the number of punctuation to be inserted is reduced to the maximum number of positions to hyphenate. 
# 'va|cuna'
````

In the same way, if we specify a number of punctuation injections lower than all the syllables boundaries available, the syllables boundaries will be randomly selected.

````python
from pyleetspeak import PuntctuationCamouflage

wrd_camo = PuntctuationCamouflage(
    word_splitting=False,
    uniform_change=True,
    hyphenate=True,
    punctuation = ["|"], 
    lang="es",
    # seed=40 # for reproducibility
)

wrd_camo.text2punctcamo("vacuna", n_inj=1)
# 'va|cuna'
````

---

### **InversionCamouflage**

Word camouflge inverting syllables order.

---

#### **Parameters**

The inversion output can be controlled using the ``max_dist`` and ``only_max_dist_inv`` parameters.
If several inversions can be applied with the same parameter, a random one is selected and applied.

- ``max_dist`` (int): Maximum distance between syllabels for inversion. 
                Example: If max_dist = 1 in "va-cu-na" only inversions va <--> cu ; cu <--> na will occur. 
                If max_dist = 2 in "va-cu-na"  inversions va <--> cu ; cu <--> na ; va <--> na will occur

- ``only_max_dist_inv`` (bool): Indicates whether you want to obtain only the inversion of max_dist or choose among
                    all inversions with the smallest possible distances up to max_dist. 
                    If True only max_dist inversion is considered for randomly selection of inversion.

---

#### **Basic Use**

````python
from pyleetspeak import InversionCamouflage

text = "vacuna"
inverter = InversionCamouflage(seed=21)
inverter.text2inversion(text, lang="es", max_dist=1, only_max_dist_inv=True)
# 'cuvana'
````

---

## **Leet NER data Generator**

This method transform an input text into a camouflaged version. The use of word camouflage usually involves camouflaging the most important words of a sentence instead of leetspeaking all the words in the text. Thus, [keyBERT](https://maartengr.github.io/KeyBERT/index.html) is used to extract the most semantically relevant words and apply them different word camouflaging methods presented above. Finally, the camouflaged entities in the output text are annotated in Spacy format.


#### **Usage**

- ``kw_model_name`` (str): Transformer model from HuggingFace Hub  used by KeyBERT for selecting the most semantically relevant words in the sentence. These words will be camouflaged.

- ``lang`` (Union[str, List[str]])): Stopwords to remove from the document. You can either pass a customized list of stop words or a ISO 639-1 code language string (e.g. en, es, ru, fr).    

- ``max_top_n`` (int): The maximum number of keywords to extract. The final number of keywords extracted will be between 0 and the input number.

- ``important_kws`` (List[str]): List of important keywords to consider during keyword extraction. 

````python
# Probably you will need additional downloads from NLTK
import nltk
nltk.download('stopwords')
nltk.download('punkt')

from pyleetspeak.Leet_NER_generator import NER_data_generator


# Create a generator object. Specifying the language and Hf model
generator_EN = NER_data_generator(
    kw_model_name="AIDA-UPM/mstsb-paraphrase-multilingual-mpnet-base-v2",
    lang="en",
    max_top_n=5,
    seed=20,
)

# Generate NER data
text = "This is an example of leetspeak text for NER data generation"

NER_data, meta_data = generator_EN.generate_data(
        sentence=text,
        important_kws = [r"\bpfizer\b", r"control\b", r"vacuna\b", r"vaccines\b"],
    )
````

The ``NER_data`` generated is in Spacy training data format. That means for each sentence we have tuple with the camouflaged sentence and a dictionariy with the starting and ending indexes along the Entity Name:

````python
[('This is an example of l£;@tspeak Ŧ£><t for NER data generation',
  {'entities': [(22, 32, 'MIX'), (33, 38, 'LEETSPEAK')]})]
````

For the sake of transparency, the ``meta_data`` variable contains all the information related to which words from the original text have been selected and which kind of word camouflaging have been applied: 

````python
OrderedDict([('sentence',
              'This is an example of leetspeak text for NER data generation'),
             ('meta',
              [{'kw': 'leetspeak',
                'init_idxs': (22, 31),
                'kw_leet': 'l£;@tspeak',
                'params': {'leetspeak-covid_basic': {'change_prb': 0.8,
                  'change_frq': 0.5,
                  'mode': 'covid_basic',
                  'get_all_combs': False,
                  'uniform_change': array(False),
                  'seed': 20,
                  'list_changes': [('a', ['@', '4', '∆', '*', '', '.', ' ']),
                   ('e', ['3', '€', '£', '%', '@', '*', '', '.', ' ']),
                   ('i', ['1', 'l', '¡', '!', "'", '*', '', '.', ' ']),
                   ('o', ['0', 'ø', '*', '', '.', ' ']),
                   ('oo', ['u', ' ']),
                   ('u', ['_', 'Ü', 'ü', '*', '.', ' '])],
                  'text_in': 'leetspeak',
                  'text_out': 'l£@tspeak'},
                 'punct_camo': {'seed': 20,
                  'uniform_change': array(True),
                  'hyphenate': array(False),
                  'word_splitting': array(False),
                  'punctuation': '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ ',
                  'lang': 'en',
                  'n_inj': 1,
                  'text_in': 'l£@tspeak',
                  'text_out': 'l£;@tspeak'}},
                'tag': 'MIX',
                'leet_idxs': (22, 32)},
               {'kw': 'text',
                'init_idxs': (32, 36),
                'kw_leet': 'Ŧ£><t',
                'params': {'leetspeak': {'change_prb': 0.8,
                  'change_frq': 0.5,
                  'mode': array('covid_intermediate', dtype='<U18'),
                  'get_all_combs': False,
                  'uniform_change': array(False),
                  'seed': 20,
                  'list_changes': [('a', ['@', '4', '∆', '*', '', '.']),
                   ('e', ['3', '€', '£', '%', '@', '*', '', '.']),
                   ('i', ['1', 'l', '¡', '!', "'", '*', '', '.']),
                   ('o', ['0', 'ø', '*', '', '.']),
                   ('oo', ['u']),
                   ('u', ['_', 'Ü', 'ü', '*', '.']),
                   ('b', ['ß', 'vb', 'bv']),
                   ('c', ['q', 'k', '©']),
                   ('d', ['t']),
                   ('f', ['ƒ', 'ph']),
                   ('h', ['#']),
                   ('k', ['₭']),
                   ('l', ['1', 'ʅ']),
                   ('m', ['ʍ']),
                   ('n', ['π', '¬']),
                   ('p', ['₱']),
                   ('r', ['₹']),
                   ('s', ['5', '$', 'z']),
                   ('t', ['7', 'Ŧ']),
                   ('v', ['b', 'vb', 'bv', '\\/', '▼']),
                   ('w', ['ω']),
                   ('x', ['><', 'kks', '×']),
                   ('y', ['¥']),
                   ('z', ['ẕ'])],
                  'text_in': 'text',
                  'text_out': 'Ŧ£><t'}},
                'tag': 'LEETSPEAK',
                'leet_idxs': (33, 38)}]),
             ('leet_sentence',
              'This is an example of l£;@tspeak Ŧ£><t for NER data generation')])
````

#### **NER data formats**

As already shown, the NER data generated is in Spacy format. Nevertheless, we provide functions to transform it to [BILUO]((https://spacy.io/api/top-level)) and [IOB](https://spacy.io/api/top-level) formats. 

````python
from pyleetspeak import format_converter

sentence_id, words, BILUO_labels, IOB_labels = format_converter.to_bilou_and_iob_format(NER_data, "en")

pd.DataFrame({
    "sentence_id": sentence_id, 
    "words": words,
    "labels": IOB_labels
})
````

|    |   sentence_id | words      | labels      |
|---:|--------------:|:-----------|:------------|
|  0 |             0 | This       | O           |
|  1 |             0 | is         | O           |
|  2 |             0 | an         | O           |
|  3 |             0 | example    | O           |
|  4 |             0 | of         | O           |
|  5 |             0 | l£;@tspeak | B-MIX       |
|  6 |             0 | Ŧ£><t      | B-LEETSPEAK |
|  7 |             0 | for        | O           |
|  8 |             0 | NER        | O           |
|  9 |             0 | data       | O           |
| 10 |             0 | generation | O           |

