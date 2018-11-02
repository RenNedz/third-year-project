import os
import fnmatch

global testing
testing = {""}

class File_manager:
	#Create next file for writing downloaded tweets to
	@classmethod
	def open_for_download(self, calling_name):
		if calling_name == "track": #can be called by 2 different files the track.py file and the download_tweets.py
			file_name = "downloaded_track_tweets1"
			len1 = 23
			testing.add("fake calling from track.py executed")
		if calling_name == "download":
			file_name = "downloaded_tweets1"
			len1 = 17
			testing.add("fake calling from download_tweets.py executed")
		count = 1
		while os.path.isfile(file_name):
			file_name = file_name[0:len1] + str(count) #Find file name that is available
			count += 1
			testing.add("while loop executed")
		out_file = open(file_name, "w",1)
		testing.add("open_for_download executed")
		return out_file

	@classmethod
	def open_next(self, calling_name):#returns true/false for there exists file, input file for calling script, output file for calling script
		if calling_name == "extract":
			pattern = 'downloaded_tweets*' # can be called by 3 scripts extract.py sentiment.py and extract_tracked.py
			file_name1 = "downloaded_tweets1"
			file_name2 = "extracted_tweets1"
			len1 = 17
			len2 = 16
		if calling_name == "sentiment":
			pattern = 'extracted_tweets*'
			file_name1 = "extracted_tweets1"
			file_name2 = "ready_to_insert_tweets1"
			len1 = 16
			len2 = 22
		if calling_name == "tracked_extract":
			pattern = "downloaded_track_tweets*"
			file_name1 = "downloaded_track_tweets1"
			file_name2 = "extracted_tweets1"
			len1 = 23
			len2 = 16
		exists = False
		files = os.listdir('.')
		for name in files:
   			if fnmatch.fnmatch(name, pattern) == True:
   				exists = True
		if exists == True:
			count = 1
			while not os.path.isfile(file_name1): #Find first occurence of file name
				count += 1
				file_name1 = file_name1[0:len1] + str(count)
			while os.path.isfile(file_name1): #Find latest occurence of file name
				count += 1
				file_name1 = file_name1[0:len1] + str(count)
			file_name1 = file_name1[0:len1] + str(count -1)
			in_file = open(file_name1, "r",1)
			count = 1
			while os.path.isfile(file_name2):
				count += 1
				file_name2 = file_name2[0:len2] + str(count)
			out_file = open(file_name2, "w",1)
			return (exists, in_file, out_file)
		else:
			return (exists, None, None)

	#used by insert_into_database.py returns true or false whether file exists, and an input file
	@classmethod
	def open_for_insertion(self):
		files = os.listdir('.')
		for name in files:
   			if fnmatch.fnmatch(name, "ready_to_insert_tweets*") == True:
   				file_name = "ready_to_insert_tweets1" #file might exist, if it does create different file
				count = 1
				while not os.path.isfile(file_name):
					file_name = file_name[0:22] + str(count)
					count += 1
				in_file = open(file_name, "r+",1)
				return (True, in_file)
		else:
			testing.add("file doesn't exist")
			return (False, None)

	#remove file from current directory
	@classmethod
	def remove_file(self, file_name):
		os.remove(file_name.name)
		file_name.close()

file_manager = File_manager()
(exists, in_file) = file_manager.open_for_insertion()
print testing