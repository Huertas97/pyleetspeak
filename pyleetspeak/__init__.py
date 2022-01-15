__version__ = "0.1.1"
__organization__ = "AIDA (http://aida.etsisi.upm.es/)"
from .LeetSpeaker import LeetSpeaker, PuntctuationCamouflage, InversionCamouflage
from .format_converter import to_bilou_and_iob_format
from .Leet_NER_generator import NER_data_generator, generate_data
from .modes import *
from .spacy_ner_formal_test import spacy_formal_test, plot_confusion_matrix