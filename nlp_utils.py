import nltk
import random
import re

#---------------------cleaning-tweet-words--------------------------------------
def clean_tweet(tweet):
	#convert to lower case:
	tweet = tweet.lower()
	#sub url with URL
	tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet)
	#convert @username to ALT_USER
	tweet = re.sub('@[^\s]+','ALT_USER',tweet)
	#remove additional whitespaces
	tweet = re.sub('[\s]+',' ',tweet)
	#replace #word with word
	tweet = re.sub(r'#([^\s]+)',r'\1',tweet)
	#trim
	tweet = tweet.strip('\'"')
	return tweet

#---------------------filtering tweet words--------------------------------------
#huuungry --> hungry
def replace_two_or_more(s):
	#look for 2 or more repetitions of character and replace with character itself
	pattern = re.compile(r"(.)\1{1,}",re.DOTALL)
	return pattern.sub(r"\1\1",s)

def get_stop_words_list(swlFilename):

	#read the stop words file and build a list
	stopWords = []
	stopWords.append('AT_USER')
	stopWords.append('URL')

	fp = open(swlFilename,'r')
	line = fp.readline()
	while line:
		word = line.strip()
		stopWords.append(word)
		line = fp.readline()
	fp.close()
	return stopWords

def get_feature_vector(tweet,stopWords):

	featureVector = []
	#split tweet into words
	words = tweet.split()

	for w in words:
		#replace two or more
		w = replaceTwoOrMore(w)
		#strip punctuation
		w = w.strip('\'"?,:!.')
		#check if the word starts with an alphabet
		val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
		#ignore if it is a stop word
		if(w in stopWords or val is None):
			continue
		else:
			featureVector.append(w.lower())
	return featureVector

#function to find the most frequent tags in tagged text
def find_tags(tag_prefix,tagged_tex):
	cfd = nltk.ConditionalFreqDist( (tag,word) for (word,tag) in tagged_text if tag.startswith(tag_prefix))
	return dict( (tag,cfd[tag].keys()[:5]) for tag in cfd.conditions() )

def document_features(document,word_features,header_string):
	document_words = set(document)
	features = {}
	for word in word_features:
		features[header_string+'(%s)' % word] = (word in document_words)
	return features
