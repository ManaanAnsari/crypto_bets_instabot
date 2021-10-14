#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 14:27:36 2021

@author: li
"""

import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.api import delete_resources_by_tag, resources_by_tag
from global_vars import cloud_name, api_key, api_secret


cloudinary.config( 
  cloud_name = cloud_name, 
  api_key = api_key, 
  api_secret = api_secret 
)


def upload_signal():
    # upload
    upload_obj = cloudinary.uploader.upload("./signal.jpg",tags="signal",public_id="signal")
    # get url
    url = cloudinary.utils.cloudinary_url("signal.jpg")
    if isinstance(url, tuple):
        url = url[0]
        if upload_obj.get("version",None):
            version = upload_obj.get("version",None)
            url = url[:-10]
            url += 'v'+str(version)+'/signal.jpg'
        return url
    return None


# delete
def delete_signals():
    response = resources_by_tag("signal")
    resources = response.get('resources', [])
    if resources:    
        print("Deleting {0:d} images...".format(len(resources)))
        delete_resources_by_tag("signal")
        print("Done!")

