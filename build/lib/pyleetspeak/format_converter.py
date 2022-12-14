from typing import List, Union, Tuple
import spacy
from spacy.training import offsets_to_biluo_tags, iob_utils
from tqdm.auto import tqdm


################## BILOU/IOB FORMAT ##########################


def get_all_tokens(doc):
    """This function unifies the tokens of different sentences from the same document
    """
    doc_tokens = []
    for sent in doc.sents:
        sent_tokens = [token.text for token in sent]
        doc_tokens.extend(sent_tokens)
    return doc_tokens


def get_all_tokens_nltk(text):
    tokens = word_tokenize(text)
    return tokens


def to_bilou_and_iob_format(data: List[List[Union[str, dict]]], lang: str = "en"):
    # Create empy nlp model. It wont do anything excepting transform text into nlp doc object
    nlp = spacy.blank(lang)
    nlp.add_pipe('sentencizer')  # tokenizer
    sentence_id = []
    words = []
    BILUO_labels = []
    IOB_labels = []
    for i, (text, annotations) in enumerate(tqdm(data, desc="BILOU/IOB formatting")):
        doc = nlp(text)
        entities = annotations["entities"]
        BILUO_tags = offsets_to_biluo_tags(doc, entities)
        IOB_tags = iob_utils.biluo_to_iob(BILUO_tags)
        tokens = get_all_tokens(doc)
        assert len(tokens) == len(BILUO_tags)
        assert len(tokens) == len(IOB_tags)

        sentence_id.extend([i]*len(tokens))
        words.extend(tokens)
        BILUO_labels.extend(BILUO_tags)
        IOB_labels.extend(IOB_tags)

        # print("Text", text)
        # print(entities)
        # print("Doc", doc)
        # print("Tokens", tokens)
        # print("Len tokens", len(tokens), "Len BILUO tags", len(BILUO_tags), "Len IOB tags", len(IOB_tags))
        # print("Tags", tags)
    return sentence_id, words, BILUO_labels, IOB_labels
