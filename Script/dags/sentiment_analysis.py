from flair.models import TextClassifier
from flair.data import Sentence
import re




def predict_sentiments(data):
    classifier = TextClassifier.load('en-sentiment')
    sentences = [Sentence(s) for s in data['tweet']]
    classifier.predict(sentences)
    sent_labels=[]
    sent_conf = []
    for s in range(0,len(sentences)):
        if sentences[s]:
            sent = str(sentences[s].labels[0])
            sent_conf.append(float(re.findall("\d+\.\d+", sent)[0]))
            sent_labels.append(" ".join(re.findall("[a-zA-Z]+", sent)))
        else:
            print(s)
    data['sentiment'] = sent_labels
    data['sentiment_confidence'] =sent_conf
    return data

