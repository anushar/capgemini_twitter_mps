import nltk
import pickle


classifiers = pickle.load(open('party_classifiers','rb'))
most_informative_features = pickle.load(open('most_informative_features','rb'))

