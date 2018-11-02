"""
REFERENCES:
    Perkins, J. (2010) Python Text Processing with NLTK 2.0 Cookbook
    Available at: http://caio.ueberalles.net/ebooksclub.org__Python_Text_Processing_with_NLTK_2_0_Cookbook.pdf
    
  Positive/Negative Word List:
        Minqing Hu and Bing Liu. "Mining and Summarizing Customer Reviews." 
        Proceedings of the ACM SIGKDD International Conference on Knowledge 
        Discovery and Data Mining (KDD-2004), Aug 22-25, 2004, Seattle, Washington, USA
        Available at: http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html
    
   Natural Language ToolKit Stopwords Corpus:
        Available at: www.nltk.org
        
    Python Documentation:
        Available at: https://docs.python.org/2/index.html
                      https://pymotw.com/2/collections/counter.html (Counter class/methods)
                      https://docs.python.org/2/library/string.html (String methods) 
"""

from nltk.corpus import stopwords   #https://pypi.python.org/pypi/nltk, a natural language processing library package
                                    #consists of 128 English stopwords or commonly used words with no sentiment (i.e. 'the', 'a', etc.)
import collections
import string
import re
import subprocess
from File_manager import File_manager
#Takes in file which has extracted tweet information
#Produces file which is ready for uploading into the database

class Sentiment:

    #searches for unicode value of an emoji - begins with \u and a mixtures of lowercase letters and digits
	def find_emoji(self, tweet):
		emoji = re.findall("\\\\u[0-9a-z]+", tweet)
		return emoji

    #removes irrevelant characters which were converted to unicode upon extraction with an empty string
    #replaces converted unicode characters with their ASCII counterpart
	def sub_unicodes(self,line):
		line = re.sub("&amp;", "&", line)
		line = line.replace("\\n", " ")
		line = line.replace("\\r", " ")
		line = re.sub("\\\u2026", "...", line)
		line = re.sub("\\\u2019", "'", line)
		line = re.sub("\\\u2014", "-", line)
		line = re.sub("\\\u2011", "-", line)
		line = re.sub("\\\u2013", "-", line)
		line = re.sub("\\\u201c", "\"", line)
		line = re.sub("\\\u201d", "\"", line)
		line = re.sub("\\\u2022", "\"", line)
		line = re.sub("\\\u2122", " TM", line)
		line = re.sub("\\\u2260", " !=", line)
		line = re.sub("\\\u\w*", "", line)
		line = re.sub("\\\\x\w*", "", line)
		line = re.sub("\\\U\w*", "", line)
		return line

    #compares each emoiji found within the tweet text to the positive emoji text file
    #if it matches an entry within said text file, it adds 2 and returns the total number found
    #returns 0 if none are found
	def check_pos_emoji(self, emoji, pos_emoji): 
		pos = 0
		for e in emoji:
			if e in pos_emoji:
				pos += 2
		return pos

    #compares each emoiji found within the tweet text to the negative emoji text file
    #if it matches an entry within said text file, it adds 2 and returns the total number found
    #returns 0 if none are found
	def check_neg_emoji(self, emoji, neg_emoji):    
		neg = 0
		for e in emoji:
			if e in neg_emoji:
				neg += 2
		return neg
		
    #determines sentiment of both text and emojis within the tweet 
	def check_sentiment(self,bow,positives,negatives): 
	    # uses integer value of the total number of matching positive and negative emojis already found within the text
	    # pos and neg will equal to 0 if none have been found
		pos = self.check_pos_emoji(emoji, pos_emoji)
		neg = self.check_neg_emoji(emoji, neg_emoji)

        ### if each word in the bag of words matches against the positive or negative word list, add 1
		for word in bow:
			if negatives.find("\n" + word[0] + "\n") != -1:
				neg += 1
			
			elif positives.find("\n" + word[0] + "\n") != -1:
				pos += 1
				
		if pos > neg:
			return 1    #return positive overall sentiment
		elif neg > pos:
			return 2    #return negative overall sentiment
		else:
			return 3    #return neutral overall sentiment
		
	#prepares tweet text by removing emojis, full stops, commas, exclamation points and question marks at the end of words
	def prepare(self, word):
		word = re.sub(r'\.', " ", word) #removes full stops
		word = re.sub(r'\,', " ", word) #removes full stops
		word = re.sub(r'\!', " ", word) #removes !
		word = re.sub(r'\?', " ", word) #removes ?
		word = re.sub(r"\\u[0-9a-z]+", "", word) #removes unicode from tweet's text
		return word
		
		
	def tokenise(self, tweet): #returns a list of only strings (text of the tweet)
		tweet = self.prepare(tweet) 
		tweet_text = tweet.lower().split() #removes whitespace and converts text to lowercase
		
		return tweet_text


	def bag_of_words(self, tweet):
		punc = list(string.punctuation) + ['rt']  #list of punctuation marks and RT (twitter retweet symbol)
		stops = set(stopwords.words('english') + punc)  #stopwords of 128 commonly used words and punctuation
		
		bag = [w for w in tweet if w not in stops and not w.isdigit()]  #bag of words with only text and no digits
		bow = collections.Counter(bag)  #creates dictionary counting number of times a word appears
		
		return bow.most_common(10)  #returns 10 most common words in the bag

#if exists is true, in file and out file are present
#if false then there is no file to read into 

(exists, in_file, out_file) = File_manager.open_next("sentiment")
if exists == True:
	check = Sentiment()
    
    #open negative words, positive words, negative emojis, positive emojis
	neg_emoji_file = open("neg_emoji.txt", "r", 1)
	pos_emoji_file = open("pos_emoji.txt", "r", 1)
	neg_emoji = neg_emoji_file.read()
	pos_emoji = pos_emoji_file.read()
	neg_emoji_file.close()
	pos_emoji_file.close()

	neg_file = open("neg.txt","r",1)
	pos_file = open("pos.txt","r",1)
	negatives = neg_file.read()
	positives = pos_file.read()
	pos_file.close()
	neg_file.close()
	for line in in_file:
        
        ##takes text of tweets
		analyse_line = line[5: line.find(" Language:")]
		
		##gets emojis
		emoji = check.find_emoji(analyse_line)
		
		##tokenises line
		content = check.tokenise(analyse_line)
		
		##creates bag of words
		bow = check.bag_of_words(content) 
		
		##determines sentiment
		sentiment = check.check_sentiment(bow,positives,negatives)
		
		##cleans up line further by removing or replacing unnecessary unicode values
		line = check.sub_unicodes(line)
		
		##if 1 is returned, sentiment is positive and writes out line to file
		if sentiment == 1:
			line = re.sub("\n", " Sentiment: Pos\n", line)
			out_file.write(line)

		##if 2 is returned, sentiment is negative and writes out line to file
		elif sentiment == 2:
			line = re.sub("\n", " Sentiment: Neg\n", line)
			out_file.write(line)
			##if 2 is returned, sentiment is neutral and writes out line to file
		elif sentiment == 3:
			line = re.sub("\n", " Sentiment: Neu\n", line)
			out_file.write(line)
	out_file.close()
	##removes in file
	#File_manager.remove_file(in_file)
	
	##restarts process
	#p = subprocess.Popen(["python", "sentiment.py"])
else:
    
    ##inserts new data into database
	p = subprocess.Popen(["python", "insert_into_database.py"])