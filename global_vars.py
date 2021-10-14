
# fb/insta creds
creds = {
    'client_id': '123', # client id from facebook app IG Graph API Test
    'client_secret' : 'shhhh!', # client secret from facebook app
    'debug':'no', # debug mode for api call
    'ig_username':'crypto_bets_', # ig username
    'access_token': 'secureRandonHash', # access token for use with all api calls
    'graph_domain': 'https://graph.facebook.com/', # base domain for api calls
    'graph_version': 'v6.0', # version of the api we are hitting
    'instagram_account_id':'123', # users instagram account id
    'page_id':'123', 
}
creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/' # base endpoint with domain and version

# conf for cloudinary
cloud_name = "cloud", 
api_key = "123", 
api_secret = "cloudsecret"


