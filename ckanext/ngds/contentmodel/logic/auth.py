''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

"""
Contains all authorization functions related to content model functionality
"""

import ckan.plugins as p


def _datastore_auth(context, data_dict):
    """
    Auth function which checks the resource update access for allowing user to access functionality.
    """
    if not 'id' in data_dict:
        data_dict['id'] = data_dict.get('resource_id')
    user = context.get('user')

    authorized = p.toolkit.check_access('resource_update', context, data_dict)

    if not authorized:
        return {
            'success': False,
            'msg': p.toolkit._('User {0} not authorized to update resource {1}'\
                    .format(str(user), data_dict['id']))
        }
    else:
        return {'success': True}


def datastore_create(context, data_dict):
    return _datastore_auth(context, data_dict)

def datastore_spatialize(context, data_dict):
    return {'success': True}

def datastore_upsert(context, data_dict):
    return _datastore_auth(context, data_dict)


def datastore_delete(context, data_dict):
    return _datastore_auth(context, data_dict)


def datastore_search(context, data_dict):
    return {'success': True}
