from twarc import Twarc
from File_manager import File_manager
#usage, takes in a file called ids with id's of tweets to hydrate.
testing = {""}
t = Twarc('4lJGm5YUrXgtwfMUmlo9L4KgH','YIYeIiZGCJpolIASa56eqLJsEa54vGKFt07CkTai3SWKoCPx3w','276679861-dgKpojdDSWRutxEG7NH2A2ZgD7xHtzcuwOisMo1T', '4ckJoGnRm5defgDegfV4opPETmarGuNQr9U6pAVEwR9sT')
out_file = File_manager.open_for_download("download") #Get file to write to
ids = open("ids", "r", 1)
for tweet in t.hydrate(ids):
	tweet = str(tweet)
	out_file.write(tweet + "\n")
	testing.add("for loop executed")
out_file.close()
ids.close()
testing.add("hydrate  executed")
print testing