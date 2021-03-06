#!/usr/bin/python

import feedparser
import datetime
import iso8601
import urllib
import time

HOST = 'http://gentle-stream-2067.herokuapp.com/'
ACCESS_TOKEN = 'AAAC0ujN1UXEBAA5nKpsSOzOurAGamZA5QVBLNLA5Uv6rFvkXFZBZCz9qUNndtGkkCEyfKPEqxvJ7qZBWto41gJXYRmWLJGzFSA3qmm1yawZDZD'
latest_access = None

#Get a list of users ... yes, this could be huge, but we are just hacking ;)
users = ['arcturus']

def get_user_commits(user):
	global latest_access
	user_feed = feedparser.parse('https://github.com/' + user + '.atom')
	print 'Got ' + user_feed.feed.title
	latest = None
	for element in user_feed.entries:
		date = iso8601.parse_date(str(element.published))
		title = str(element.title)
		if title.find('pushed') != -1 and is_date_bigger_than(date, latest_access) :
			#Is this the latest interaction?
			project = title[title.index('/') + 1:]
			commit = str(element.links[0].href)[str(element.links[0].href).index('...') + 3:]		
			url = HOST + 'projects/' + user + '/' + project + '/' + commit
			print 'Got to notify for url: ' + url
			params = {}
			params['access_token'] = ACCESS_TOKEN
			params['project'] = url
			params = urllib.urlencode(params)
			f = urllib.urlopen("https://graph.facebook.com/me/_codebook:Commit", params)
			print "1 " + str(latest_access)
			if latest == None:
				latest = date
			elif is_date_bigger_than(date, latest):
				latest = date
			#print 'New push!: \n' + str(element)
			print "2 " + str(latest_access)
			
	if latest != None:
		print 'Latest interaction was: ' + str(latest)
		latest_access = latest
		print "3 " + str(latest_access)
			
def is_date_bigger_than(date1, date2):
	"""
		Given two dates, just say if one is bigger than the other one.
	"""
	if date2 is None:
		date2 = datetime.datetime(1970, 1, 1, 0, 0, 0)
	dt1 = date1.replace(tzinfo=None)
	dt2 = date2.replace(tzinfo=None)
	if dt1 - dt2 > datetime.timedelta(seconds = 0):
		return True
	return False
	
def main():
	while True:
		for user in users:
			get_user_commits(user)
			#get_user_commits(user, datetime.datetime(2011, 12, 30, 20, 43, 20))
		time.sleep(15)
	
if __name__ == '__main__':
	main()	