import os.path
import subprocess
from twarc import Twarc
from File_manager import File_manager
#usage, takes in a file called tags with name or hashtag to search by per line.


t = Twarc('4lJGm5YUrXgtwfMUmlo9L4KgH','YIYeIiZGCJpolIASa56eqLJsEa54vGKFt07CkTai3SWKoCPx3w','276679861-dgKpojdDSWRutxEG7NH2A2ZgD7xHtzcuwOisMo1T', '4ckJoGnRm5defgDegfV4opPETmarGuNQr9U6pAVEwR9sT')
in_file = open("tags","r" , 1) #open file which contains tweets hashtags or word by which to download
file_counter = 0
for tag in in_file:
    count = 0
    out_file = File_manager.open_for_download("download") #open file to write to
    for tweet in t.search(tag):
        tweet = str(tweet) #stringify tweet 
        out_file.write(tweet + "\n")#write tweet out one tweet per line
        if count == 10:
        	break
        count += 1
    out_file.close()
