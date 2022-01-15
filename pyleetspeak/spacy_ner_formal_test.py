###############################################################
# Code inspired by the gratest:
#     - PYDH Youtbe Channel: https://www.youtube.com/watch?v=k1FtpADlusE
#     - Dulaj Rajitha: https://dulaj.medium.com/confusion-matrix-visualization-for-spacy-ner-9e9d99120ee9
###############################################################

from spacy.training import offsets_to_biluo_tags
from matplotlib import pyplot
import numpy
from sklearn.metrics import confusion_matrix
from tqdm.auto import tqdm

class spacy_formal_test(object):
  def __init__(self, nlp, docs):
    self.nlp = nlp
    self.docs = docs

  def get_cleaned_label(self, label: str):
      if "-" in label: # -
          return label.split("-")[1]
      else:
          return label
      
  def create_total_target_vector(self):
      target_vector = []
      for doc in self.docs:
          # print (doc)
          new = self.nlp.make_doc(doc[0])
          entities = doc[1]["entities"]
          bilou_entities = offsets_to_biluo_tags(new, entities)
          final = []
          for item in bilou_entities:
              final.append(self.get_cleaned_label(item))
          target_vector.extend(final)
      return target_vector

  def create_prediction_vector(self, text):
      return [self.get_cleaned_label(prediction) for prediction in self.get_all_ner_predictions(text)]

  def create_total_prediction_vector(self):
      prediction_vector = []
      for doc in tqdm(self.docs, desc="Predictions"):
          prediction_vector.extend(self.create_prediction_vector(doc[0]))
      return prediction_vector

  def get_all_ner_predictions(self, text):
      doc = self.nlp(text)
      entities = [(e.start_char, e.end_char, e.label_) for e in doc.ents]
      bilou_entities = offsets_to_biluo_tags(doc, entities)
      return bilou_entities



  def get_model_labels(self):
      labels = list(self.nlp.get_pipe("ner").labels)
      labels.append("O")
      return sorted(labels)

  def get_dataset_labels(self):
      return sorted(set(self.create_total_target_vector()))

  def generate_confusion_matrix(self): 
      classes = sorted(set(self.create_total_target_vector()))
      y_true = self.create_total_target_vector()
      y_pred = self.create_total_prediction_vector()
      # print (y_true)
      # print (y_pred)
      return confusion_matrix(y_true, y_pred, labels=classes), classes


def plot_confusion_matrix(conf_matrix, normalize=False, cmap=pyplot.cm.Blues, title:str = 'Confusion Matrix, for SpaCy NER'):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
   

    # Compute confusion matrix
    cm, classes = conf_matrix
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, numpy.newaxis]

    fig, ax = pyplot.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=numpy.arange(cm.shape[1]),
           yticks=numpy.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    pyplot.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return cm, ax, pyplot

