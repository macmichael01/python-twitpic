Version 2.0
===========

*NOTE*: The TwitPicOAuthClient does NOT support fetching an access_token. Use your 
favorite Twitter API Client to retrieve this. An access_token is required in most API calls.

GET based calls do not require any keys or tokens but for the rest of the API calls,
they are required.

There are 4 main methods that can be called. read, create, update, and remove which are your 
GET, POST, PUT, and DELETE methods.


INSTALLATION:
============

	sudo pip install python-twitpic

- OR::

	git clone https://github.com/macmichael01/python-twitpic;
	cd python-twitpic;
	sudo python setup.py install


USAGE:
=====

	import twitpic
	twitpic = twitpic.TwitPicOAuthClient(
		consumer_key = CONSUMER_KEY,
		consumer_secret = CONSUMER_SECRET,
		access_token = "oauth_token=%s&oauth_token_secret=%s"  % (USER_TOKEN, USER_TOKEN_SECRET),
		service_key = SERVICE_KEY
	)
	# methods - read, create, update, remove    
	response = twitpic.create(METHOD_CALL, PARAMS)
	print response

*NOTE*: importing python-twitpic can now be done as follows:

	import twitpic
	
- OR::
	
	from twitpic import twitpic2


COMMAND-LINE USAGE:
==================

*NOTE*: Bash auto complete script FTW! Command also requires python-2.7 to use.

usage: twitpic [-h] [-m MESSAGE]
               consumer_key consumer_secret access_token service_key file

Python-TwitPic commandline utility.

positional arguments:
  consumer_key          Twitter Consumer API Key
  consumer_secret       Twitter Consumer API Kecret
  access_token          Twitter Access Token
  service_key           Twitpic API Key
  file                  Path to Image File.

optional arguments:
  -h, --help            show this help message and exit
  -m MESSAGE, --message MESSAGE
                        The tweet that belongs to the image.


CHANGELOG:
==========
2-24-2012: TwitPic Client API V1.0 is now officially deprecated.
