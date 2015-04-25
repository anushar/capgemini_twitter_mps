import nltk
import random
import re




#---------------------PREPROCESSING--TWEET--WORDS---------------------------------------
def processTweet(tweet):
	
	#convert to lower case:
	tweet = tweet.lower()
	
	#convert www.* or https?://* to URL
	
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

#---------------------FILTERING--TWEET--WORDS---------------------------------------
#huuungry --> hungry
def replaceTwoOrMore(s):
	#look for 2 or more repetitions of character and replace
	#with character itself
	pattern = re.compile(r"(.)\1{1,}",re.DOTALL)
	return pattern.sub(r"\1\1",s)
	
def getStopWordsList(swlFilename):
	
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

def getFeatureVector(tweet,stopWords):

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
def findtags(tag_prefix,tagged_tex):
	
	cfd = nltk.ConditionalFreqDist( (tag,word) for (word,tag) in tagged_text if tag.startswith(tag_prefix))
	return dict( (tag,cfd[tag].keys()[:5]) for tag in cfd.conditions() ) 
	



def document_features(document,word_features):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	    #if word in document_words:
		#   features['contains(%s)' % word] = True
	return features
