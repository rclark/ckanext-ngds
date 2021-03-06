''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

from geoserver.catalog import Catalog
from pylons import config as ckan_config
import re

class Geoserver(Catalog):

    @classmethod
    def from_ckan_config(cls):
        """
        Setup the Geoserver Catalog from CKAN configuration

        @param cls: This class.
        @return: a Geoserver catalog
        """
        url = ckan_config.get("geoserver.rest_url", "http://localhost:8080/geoserver/rest")

        # Look for user information in the geoserver url
        userInfo = re.search("://(?P<auth>(?P<user>.+?):(?P<pass>.+?)@)?.+", url)
        user = userInfo.group("user") or "admin"
        pwd = userInfo.group("pass") or "geoserver"

        # Remove it from the connection URL if it was there
        url = url.replace(userInfo.group("auth") or "", "")

        # Make the connection
        return cls(url, username=user, password=pwd)

    def default_workspace(self):
        """
        Get a default workspace -- create if it does not exist

        @return: workspace instance
        """

        name = ckan_config.get("geoserver.workspace_name", "ngds")
        uri = ckan_config.get("geoserver.workspace_uri", "http://localhost:5000/ngds")

        ngds_workspace = self.get_workspace(name)
        if ngds_workspace is None:
            ngds_workspace = self.create_workspace(name, uri)
        return ngds_workspace

    def default_datastore(self):
        """
        Get default datastore, create if it does not exist

        @return: datastore instance
        """

        # Extract values from development.ini file
        datastore_url = ckan_config.get('ckan.datastore.write_url','postgresql://ckanuser:pass@localhost/datastore')

        # Extract connection details
        pattern = "://(?P<user>.+?):(?P<pass>.+?)@(?P<host>.+?)/(?P<database>.+)$"
        details = re.search(pattern, datastore_url)

        # Check if the default datastore exists
        store_name = details.group("database")
        default_ws = self.default_workspace()
        try:
            ds = self.get_store(store_name, default_ws)
        except Exception as ex:
            # Doesn't exist. Create it and update the connection parameters
            ds = self.create_datastore(store_name, default_ws)
            ds.connection_parameters.update(
                host=details.group("host"),
                port="5432",
                database=details.group("database"),
                user=details.group("user"),
                passwd=details.group("pass"),
                dbtype="postgis"
            )
            self.save(ds)

        # Return it
        return ds
