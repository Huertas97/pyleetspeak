__version__ = "0.3.9"
__organization__ = "AIDA (http://aida.etsisi.upm.es/)"
from .LeetSpeaker import LeetSpeaker
from .PunctuationCamouflage import PunctuationCamouflage
from .InversionCamouflage import InversionCamouflage
from .format_converter import to_bilou_and_iob_format
from .Leet_NER_generator import NER_data_generator
from .modes import *
from .spacy_ner_formal_test import spacy_formal_test, plot_confusion_matrix
from .WordCamouflage_Augmenter import augmenter
import nltk

nltk.download("stopwords")
nltk.download("punkt")
