
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  3 17:07:54 2021

@author: li
"""


import requests
import json
import time
from global_vars import creds


def getCreds() :
    return creds


def makeApiCall( url, endpointParams, type ) :
	""" Request data from endpoint with params
	
	Args:
		url: string of the url endpoint to make request from
		endpointParams: dictionary keyed by the names of the url parameters


	Returns:
		object: data from the endpoint

	"""

	if type == 'POST' : # post request
		data = requests.post( url, endpointParams )
	else : # get request
		data = requests.get( url, endpointParams )

	response = dict() # hold response info
	response['url'] = url # url we are hitting
	response['endpoint_params'] = endpointParams #parameters for the endpoint
	response['endpoint_params_pretty'] = json.dumps( endpointParams, indent = 4 ) # pretty print for cli
	response['json_data'] = json.loads( data.content ) # response data from the api
	response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 ) # pretty print for cli

	return response # get and return content


def debugAccessToken( params ) :
	""" Get info on an access token 
	
	API Endpoint:
		https://graph.facebook.com/debug_token?input_token={input-token}&access_token={valid-access-token}
	Returns:
		object: data from the endpoint
	"""

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['input_token'] = params['access_token'] # input token is the access token
	endpointParams['access_token'] = params['access_token'] # access token to get debug info on

	url = params['graph_domain'] + '/debug_token' # endpoint url

	return makeApiCall( url, endpointParams, params['debug'] ) # make the api call


def getLongLivedAccessToken( params ) :
	""" Get long lived access token
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}
	Returns:
		object: data from the endpoint
	"""

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['grant_type'] = 'fb_exchange_token' # tell facebook we want to exchange token
	endpointParams['client_id'] = params['client_id'] # client id from facebook app
	endpointParams['client_secret'] = params['client_secret'] # client secret from facebook app
	endpointParams['fb_exchange_token'] = params['access_token'] # access token to get exchange for a long lived token

	url = params['endpoint_base'] + 'oauth/access_token' # endpoint url

	return makeApiCall( url, endpointParams, params['debug'] ) # make the api call


def createMediaObject( params ) :
	""" Create media object
	Args:
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access-token}
		https://graph.facebook.com/v5.0/{ig-user-id}/media?video_url={video-url}&caption={caption}&access_token={access-token}
	Returns:
		object: data from the endpoint
	"""

	url = params['endpoint_base'] + params['instagram_account_id'] + '/media' # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['caption'] = params['caption']  # caption for the post
	endpointParams['access_token'] = params['access_token'] # access token

	if 'IMAGE' == params['media_type'] : # posting image
		endpointParams['image_url'] = params['media_url']  # url to the asset
	else : # posting video
		endpointParams['media_type'] = params['media_type']  # specify media type
		endpointParams['video_url'] = params['media_url']  # url to the asset
	
	return makeApiCall( url, endpointParams, 'POST' ) # make the api call


def getMediaObjectStatus( mediaObjectId, params ) :
	""" Check the status of a media object
	Args:
		mediaObjectId: id of the media object
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-container-id}?fields=status_code
	Returns:
		object: data from the endpoint
	"""

	url = params['endpoint_base'] + '/' + mediaObjectId # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['fields'] = 'status_code' # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	return makeApiCall( url, endpointParams, 'GET' ) # make the api call


def publishMedia( mediaObjectId, params ) :
	""" Publish content
	Args:
		mediaObjectId: id of the media object
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}
	Returns:
		object: data from the endpoint
	"""

	url = params['endpoint_base'] + params['instagram_account_id'] + '/media_publish' # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['creation_id'] = mediaObjectId # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token

	return makeApiCall( url, endpointParams, 'POST' ) # make the api call


def getContentPublishingLimit( params ) :
	""" Get the api limit for the user
	Args:
		params: dictionary of params
	
	API Endpoint:
		https://graph.facebook.com/v5.0/{ig-user-id}/content_publishing_limit?fields=config,quota_usage
	Returns:
		object: data from the endpoint
	"""

	url = params['endpoint_base'] + params['instagram_account_id'] + '/content_publishing_limit' # endpoint url

	endpointParams = dict() # parameter to send to the endpoint
	endpointParams['fields'] = 'config,quota_usage' # fields to get back
	endpointParams['access_token'] = params['access_token'] # access token
	return makeApiCall( url, endpointParams, 'GET' ) # make the api call


def upload_post(url):
    params = getCreds() # get creds from defines
    params['media_type'] = 'IMAGE' # type of asset
    params['media_url'] = url #'https://justinstolpe.com/sandbox/ig_publish_content_img.png' # url on public server for the post
    
    hash_tags = ' #cryptocurrency #cryptocurrencies #cryptomarket #cryptoexchange #cryptotrader #crypto #bitcoin #binance #cryptotrading #algotrading #trading #tradingstrategy #tradingsignals #tradingtips '
    hash_tags += ' #eth #ethereum '
    binance_link = '' #' https://www.binance.com/en/register?ref=WE3W5OZ0 '
    
    caption = "Long signal generated "+binance_link+hash_tags
    
    params['caption'] = caption
    
    
    imageMediaObjectResponse = createMediaObject( params ) # create a media object through the api
    imageMediaObjectId = imageMediaObjectResponse['json_data']['id'] # id of the media object that was created
    imageMediaStatusCode = 'IN_PROGRESS';
    
    print( "\n---- IMAGE MEDIA OBJECT -----\n" ) # title
    print( "\tID:" ) # label
    print( "\t" + imageMediaObjectId ) # id of the object
    
    while imageMediaStatusCode != 'FINISHED' : # keep checking until the object status is finished
    	imageMediaObjectStatusResponse = getMediaObjectStatus( imageMediaObjectId, params ) # check the status on the object
    	imageMediaStatusCode = imageMediaObjectStatusResponse['json_data']['status_code'] # update status code
    
    	print( "\n---- IMAGE MEDIA OBJECT STATUS -----\n" ) # display status response
    	print( "\tStatus Code:" ) # label
    	print( "\t" + imageMediaStatusCode ) # status code of the object
    
    	time.sleep( 5 ) # wait 5 seconds if the media object is still being processed
    
    publishImageResponse = publishMedia( imageMediaObjectId, params ) # publish the post to instagram
    
    print( "\n---- PUBLISHED IMAGE RESPONSE -----\n" ) # title
    print( "\tResponse:" ) # label
    print( publishImageResponse['json_data_pretty'] ) # json response from ig api







