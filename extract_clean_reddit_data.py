

''' extract_clean_reddit_data.py: Extracts the post heading and body of comments extracted from the subreddit 
Usage: extract_reddit_data.py <data_directory>
Returns: File with the comment title and body on separate lines and the body sentence tokenized.'''

__author__ = " Sarah McLeod"
__version__ = "1.0.1"
__email__ = "smcleod@coli.uni-saarland.de"

import os, sys, re, json
import nltk

BOT_STRINGS = ['BotsByLiam', 'This bot was created by devious1087']
		
def main():
	data_dir = sys.argv[1]
	# Extact the post heading and the body of the comment.
	# Print to a new file with each post title and body as a new line
	#cleaned_comment_data = {}
	for eachFile in os.listdir(data_dir):
		#print (eachFile)
		df = open(os.path.join(data_dir, eachFile), 'r')
		json_data = json.load(df)
		ef = open(re.sub('json', 'txt', eachFile), 'w')

		
		try:
			for x in range(0, len(json_data['data']['children'])):
				title = json_data['data']['children'][x]['data']['link_title']
				body = json_data['data']['children'][x]['data']['body']
				#print (title)
				#print (body)
				#If the post self identifies as a bot, remove from the data set.
				if re.search("I[' ]a?m a bot", body) != None:
					#print ('removing: ', body, ' from data set')
					pass
				else:
					# For other specific instances of bots.
					if any(x in body for x in BOT_STRINGS):
						#print ('removing', body, ' from data set')
						pass
					else:
						body = re.sub('\n', ' ', body)
						# Remove all references to web pages in the context of the tweet
						body = re.sub('http\S+', '', body)
						body = re.sub('www\S+', '', body)
						# Sentence tokenize body , so I can add sentence tags later
						sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
						sent_tok_commments = sent_tokenizer.tokenize(body)
						sent_tok_titles = sent_tokenizer.tokenize(title)
						#print (sent_tok_commments)
						sent_tagged_comments = 	'<S>'.join([x.strip() for x in sent_tok_commments])
						sent_tagged_titles = '<S>'.join([x.strip() for x in sent_tok_titles])
						print (sent_tagged_titles)
						# 
						#if re.search('[.!?]$', sent_tagged_comments) != None:
						#	sent_tagged_comments = sent_tagged_comments + '<S>'

						#print (sent_tagged_comments)
						ef.write('Title: ' + sent_tagged_titles + '<S>\n')
						ef.write('Body: ' + sent_tagged_comments + '<S>\n')
		
		#Ignore when a request didn't go through
		except KeyError:
			#print (data)
			pass

		ef.close()

if __name__ == '__main__':
	main()