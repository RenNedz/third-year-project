import os.path
from twarc import Twarc
from File_manager import File_manager
#usage, takes in a file called tags with name or hashtag to search by per line.

t = Twarc('4lJGm5YUrXgtwfMUmlo9L4KgH','YIYeIiZGCJpolIASa56eqLJsEa54vGKFt07CkTai3SWKoCPx3w','276679861-dgKpojdDSWRutxEG7NH2A2ZgD7xHtzcuwOisMo1T', '4ckJoGnRm5defgDegfV4opPETmarGuNQr9U6pAVEwR9sT')
out_file = File_manager.open_for_download("track")
in_file = open("tags", "r", 1)
for tag in in_file:
    print tag
    for tweet in t.filter(track=tag):
        tweet = str(tweet)
        out_file.write(tweet + "\n")
out_file.close()
in_file.close()