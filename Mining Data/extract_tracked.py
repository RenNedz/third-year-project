#!/usr/bin/env python
from langdetect import detect #google language detection, ported to python. Link:https://pypi.python.org/pypi/langdetect?
import re
from File_manager import File_manager

class Extraction_tracked:
#Very similary to Extraction class. However the format the data is presented in is different so differenct spacing is used meaning extraction must be different.

    global pro_brexit 
    pro_brexit = ["#beleave", "#betteroffout", "#britainout","#eupol", "#grassrootsout", "#leaveeu", "#labourleave","#loveeuropeleaveeu","#no2eu","#notoeu","#projectfact","#voteleave","#voteout","#euout","#noeu","@vote_leave","@vote_LeaveMedia","@britinfluence", "@lsebrexitvote", "@leaveeuofficial", "@whatukthinks", "@grassroots_out", "@euromove", "choice4britain", "@brexitwatch"]
    global pro_stay
    pro_stay = ["#betteroffin", "#bremain", "#brexshit", "#brexitfears", "#greenerin", "#labourin", "#leadnotleave", "#remain", "#remaineu", "#strongerin", "#ukandeu", "#yes2eu", "#intogether", "@ukandeu", "@sayyes2europe"]

    def getLocation(self, location, out_file):
    	location = location.lower()
        for s in english:
            if location.count(s) != 0:
                out_file.write("England City/Town: " + s.title())
                return

        for s in scottish:
            if location.count(s) != 0:
                out_file.write("Scotland City/Town: " + s.title())
                return

        for s in welsh:
            if location.count(s) != 0:
                out_file.write("Wales City/Town: " + s.title())
                return

        for s in northern_irish:
            if location.count(s) != 0:
                out_file.write("N. Ireland City/Town: " + s.title())
                return

        for s in irish:
            if location.count(s) != 0:
                out_file.write("Ireland City/Town: " + s.title())
                return

        if location.count("england") != 0:
            out_file.write("England City/Town: None")
            return

        if location.count("scotland") != 0:
            out_file.write("Scotland City/Town: None")
            return

        if location.count("wales") != 0:
            out_file.write("Wales City/Town: None")
            return

        if location.count("northern ireland") != 0 or location.count("n. ireland") != 0:
            out_file.write("N. Ireland City/Town: None")
            return

        if location.count("ireland") != 0:
            out_file.write("Ireland City/Town: None")
            return

        if location.count("britain") != 0 or location.count("uk") or location.count("united kingdom"):
            out_file.write("Great Britain City/Town: None")
            return

        for s in capitals:
            country = s[0:s.find(",")]
            city = s[s.find(",") + 2: len(s)]
            if location.count(country) != 0 or location.count(city) != 0:
                out_file.write(country.title())
                out_file.write(" City/Town: ")
                if location.count(city) != 0:
                    out_file.write(city.title())
                else:
                    out_file.write("None")
                return

        out_file.write("None City/Town: None")

    def stance(self, out_file, text):
        out_file.write(" Stance: ")
        brexit = 0
        stay = 0
        for word in pro_brexit:
            text = text.lower()
            count = text.count(word)
            if count != -1:
                brexit += count
        for word in pro_stay:
            count = text.count(word)
            if count != -1:
                stay += count
        if brexit > stay:
            out_file.write("Pro_brexit")
        elif stay > brexit:
            out_file.write("Pro_stay")
        elif brexit == stay:
            out_file.write("None")

    def prepare(self, word):
        word = re.sub("u\"", "'", word)
        word = re.sub("\"", "'", word)
        word = re.sub("u'", "'", word)
        return word

    def text(self, out_file, word):
        #get tweet content
        global abandonTweet
        abandonTweet= False
        start = word.find("'text': '") #find tweet text
        start = start + 9 #Add 9 as that's the number of characters before the tweet starts
        end = word.find("', 'is") #find end of tweet text
        try:
            lang = detect(word[start:end]) #detect is a method of langdetect, detects which language the tweet is in
            if lang != "en":
                raise Exception
            global text
            text = word[start:end]
            out_file.write("Text:")
            out_file.write(word[start:end]) #write tweet text to file, substring between start and end
            out_file.write(" Language:")
            out_file.write(lang) #detect is a method of langdetect, detects which language the tweet is in
            out_file.write(" ")
        except Exception:
            abandonTweet = True

    #get id of tweet
    def id(self, out_file, word):
        #get tweet ID
        global currentId
        out_file.write("Id:")
        start = word.find("'id': ") 
        start = start + 6 
        end = word.find(", 'fav") 
        currentId = word[start:end]
        out_file.write(currentId)
        out_file.write(" ")

    def mentions(self, out_file, word):
        #Get users mentioned id, screen_name and username
        out_file.write("Mentions:")
        count = 1
        isMentions = False
        start = word.find("{'user_mentions': [")
        start = start + 19
        first = True
        while word[start] != "]":
                if first == True:#first mention,will have different spacing to subsequent mentions
                    start = start + 8
                    isMentions = True
                else:
                    start = 10
                end = word.find(", 'indices': [")
                label = "M_id" + str(count) + ": "
                out_file.write(label)
                out_file.write(word[start:end]) #id of user mentioned
                out_file.write(" ")

                start = word.find(", 'screen_name': '")
                start = start + 18
                end = word.find("', 'name':")
                label = "M_sc_name" + str(count) + ": "
                out_file.write(label)
                out_file.write(word[start:end]) #screen_name
                out_file.write(" ")

                start = end + 12 #user name field is after screen_name field
                s = word[start:start + 150] #used to find user name
                sEnd = s.find("}") -1 #find where user name ends
                end = start + sEnd
                label = "M_user_name" + str(count) + ": "
                out_file.write(label)
                out_file.write(word[start:end])
                out_file.write(" ")
                start = end + 1
                word = word[start:len(word)]
                start = 1
                first = False
                count += 1
        if isMentions == True:
                    out_file.write(" ")
        else:
                    out_file.write("null ")

    def hashtags(self, out_file, word):
        #Get hashtags
        out_file.write("Hashtags:")
        count = 1
        isHashtags = False
        start = word.find(", 'hashtags': [")
        start = start + 14
        first = True
        while word[start + 1] != "]":
                    if first == True:#first hashtag will have different spacing to subsequent hashtags
                        isHashtags = True
                        word = word[start : len(word)]
                        start = word.find("text': '")
                        start = start + 8
                        end = word.find("'}")
                        label = "Htag" + str(count) + ": "
                        out_file.write(label)
                        out_file.write(word[start:end])
                        out_file.write(" ")
                        start = end + 1
                        first = False
                        count += 1
                    else:
                        word = word[start : len(word)]
                        start = word.find("text': '")
                        start = start + 8
                        end = word.find("'}")
                        label = "Htag" + str(count) + ": "
                        out_file.write(label)
                        out_file.write(word[start:end])
                        out_file.write(" ")
                        start = end + 1
                        count += 1
        if isHashtags == True:
                    out_file.write(" ")
        else:
                    out_file.write("null ")

    def retweet_count(self, out_file, word):
        out_file.write("RT count:")
        correctId = False
        while correctId == False: #if multiple retweet fields, it's always the last one
            end = word.find("retweet_count': ") -4 #find number of retweets
            start = end -6
            while word[start:end] != "id_str":
                start -= 1
                end -= 1
            start += 9
            end = start + 1
            while word[end] != "'":
                end += 1
            if word[start + 1 :end] == currentId: #if Id matches that of the user, it is the correct retweet_count
                correctId = True
                start = word.find("retweet_count': ") + 16
                word = word[start:len(word)]
            else:
                word = word[word.find("retweet_count': ") + 16:len(word)] 
        out_file.write(word[0:word.find(",")])
        out_file.write(" ")

    def location(self, out_file, word):
        out_file.write("Country:")
        while word.count("location': ") != 0:
            start = word.find("location': ")
            word = word[start + 12:len(word)]
            end = word.find("'")
        if word[0:end] == "one, ":
            self.getLocation(word[0:end -2], out_file)
        else:
            self.getLocation(word[0:end], out_file)
        out_file.write(" ")

    def date(self, out_file, word):
        out_file.write("Date:")
        while word.count("created_at': '") != 0:
            start = word.find("created_at': '")
            word = word[start + 18:len(word)]
            end = word.find("'")
        dateToCrop = word[0:end]
        start = dateToCrop.find("+")
        minus = dateToCrop.find("-")
        if minus < start and minus != -1:
            start = dateToCrop.find("-")
        start = start + 5 #after the plus or minus, there are 5 characters before the year
        out_file.write(word[0:6])
        out_file.write(word[start:end])

#open file called in, for reading, with buffer enabled
(exists, in_file, out_file) = File_manager.open_next("tracked_extract")

#prepare lists for checking location
global english, scottish, welsh, northern_irish, irish, countries, capitals
english = open("english_cities", "r", 1).readlines()
english = [x.strip() for x in english]
scottish = open("scottish_cities", "r", 1).readlines()
scottish = [x.strip() for x in scottish]
welsh = open("welsh_cities","r",1).readlines()
welsh = [x.strip() for x in welsh]
northern_irish = open("northern_irish_cities","r",1).readlines()
northern_irish = [x.strip() for x in northern_irish]
irish = open("irish_cities","r",1).readlines()
irish = [x.strip() for x in irish]
countries = open("countries","r",1).readlines()
countries = [x.strip() for x in countries]
capitals = open("capital_cities", "r",1).readlines()
capitals = [x.strip() for x in capitals]
if exists == True:
    word = in_file.read()
    in_file.close()
    extraction = Extraction_tracked()
    word = extraction.prepare(word)
    try: #Last time the loop runs causes index out of bounds error. We suppress this and move on to close the file
        while word[0] == '{':
            if word[0:4] == "{'li":
                word = word[word.find("\n") + 1: len(word)]
            else:
                currentId = "empty" #reset id of current tweet, needed for identification for extraction of retweet_count
                currentTweet = word[0:word.find("\n")]
                word = word[word.find("\n") + 1: len(word)]
                extraction.text(out_file, currentTweet)
                if abandonTweet == False: #If tweet has no text, e.g. just a link, it is not recorded
                    extraction.id(out_file, currentTweet)
                    extraction.mentions(out_file, currentTweet)
                    extraction.hashtags(out_file, currentTweet)
                    extraction.retweet_count(out_file, currentTweet)
                    extraction.location(out_file, currentTweet)
                    extraction.date(out_file, currentTweet)
                    extraction.stance(out_file, text)
                    out_file.write("\n")
    except IndexError:
        pass
    out_file.close()
    File_manager.remove_file(in_file)
