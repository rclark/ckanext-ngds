''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

'''
Created on Apr 12, 2013

@author: xig3
'''

import urllib2, sys, simplejson

from ContentModel_Definitions import *
from ContentModel_Utilities   import *
import logging
log = logging.getLogger(__name__)

playground = ContentModel_Playground()

def load_schema (schema_uri, version_string):
    global playground
    log.debug("about to start schema reading")
    
    remotefile = urllib2.urlopen("http://schemas.usgin.org/contentmodels.json")
    #remotefile = urllib2.urlopen("file:///home/xig3/workspace/ModelValidation/samples/contentmodels.json")
    result = simplejson.load(remotefile)
    schemaList = [rec for rec in result if rec['uri'] == schema_uri]

    versions = schemaList[0]['versions']
    version = [rec for rec in versions if rec['version'] == version_string]

    field_info_list = version[0]['field_info']

    for field_info in field_info_list:
        if ((field_info['name'] is None) and ((len(field_info['type'])==0) or (field_info['type'].isspace()))):
            log.debug("found a undefined field: " + str(field_info))
            continue
        else: 
            playground.fieldModelList.append(ContentModel_FieldInfoCell(field_info['optional'], field_info['type'], field_info['name'], field_info['description']))

    log.debug("about to finish schema reading, find " + str(len(playground.fieldModelList)) + " field information")
# def load_schema (schema_uri, version_string)

def load_csv(csv_filename):
    global playground
    log.debug("about to start CSV reading")
    
    csv_data = ContentModel_CSVData(csv_filename)
    
    try:
        header = csv_data.csv_reader.next()
        playground.dataHeaderList = [x.strip() for x in header]
        
        for row in csv_data.csv_reader:
            new_row = [x.strip() for x in row]
            playground.dataListList.append(new_row)
    except csv.Error as e:
        sys.exit("file %s, line %d: %s" %(csv_filename, csv_data.csv_reader.line_num, e))

    log.debug("about to finish CSV reading")
# def load_csv(csv_filename)

def validate_existence():
    global playground
    log.debug("about to start field existence checking")
    
    # build link between dataHeaderList and fieldInfoList
    # fieldInfo_index = linkToFieldInfoFromHeader[headaer_index]
    linkToFieldInfoFromHeader = []
    for header in playground.dataHeaderList:
        try:
            index = [i for i, field in enumerate(playground.fieldModelList) if field.name == header]
            linkToFieldInfoFromHeader.append(index[0])
        except:
            log.debug("header: %s couldn't be found in the field_info" % header)
        
    OptionalFalseIndex = []
    for i in xrange(len(playground.dataHeaderList)):
        if   playground.fieldModelList[linkToFieldInfoFromHeader[i]].optional == False:
            OptionalFalseIndex.append(i)
    log.debug("OptionalFalseIndex: %s" % OptionalFalseIndex)
    
    for jd in xrange(len(playground.dataListList)):
        for i in xrange(len(OptionalFalseIndex)):
            data = playground.dataListList[jd][OptionalFalseIndex[i]]
            if (len(data)==0) or (data.isspace()):
                log.debug("cell (%d,%d): %s (field %s) is defined as optional false" % (jd+2, i+1, data, playground.dataHeaderList[OptionalFalseIndex[i]]))

    log.debug("about to finish field existence checking")
# def validate_existence()

def validate_numericType():
    global playground
    log.debug("about to start numeric data type checking")
    
    # build link between dataHeaderList and fieldInfoList
    # fieldInfo_index = linkToFieldInfoFromHeader[headaer_index]
    linkToFieldInfoFromHeader = []
    for header in playground.dataHeaderList:
        index = [i for i, field in enumerate(playground.fieldModelList) if field.name == header]
        linkToFieldInfoFromHeader.append(index[0])
    
    IntTypeIndex = []
    DoubleTypeIndex = []
    for i in xrange(len(playground.dataHeaderList)):
        if   playground.fieldModelList[linkToFieldInfoFromHeader[i]].typeString == 'int':
            IntTypeIndex.append(i)
        elif playground.fieldModelList[linkToFieldInfoFromHeader[i]].typeString == 'double':
            DoubleTypeIndex.append(i)
    log.debug("IntTypeIndex: %s and DoubleTypeIndex: %s" % (IntTypeIndex, DoubleTypeIndex))
    
    for jd in xrange(len(playground.dataListList)):
        # check the int type
        for i in xrange(len(IntTypeIndex)):
            data = playground.dataListList[jd][IntTypeIndex[i]]
            if isInteger(data) == False:
                if len(data) == 0:
                    log.debug("cell (%d,%d): null (field %s) is expected to be an Integer" % (jd+2, i+1, playground.dataHeaderList[IntTypeIndex[i]]))
                else:
                    log.debug("cell (%d,%d): %s (field %s) is expected to be an Integer" % (jd+2, i+1, data, playground.dataHeaderList[IntTypeIndex[i]]))
                   
        # check the double type
        for i in xrange(len(DoubleTypeIndex)):
            data = playground.dataListList[jd][DoubleTypeIndex[i]]
            if isNumber(data) == False:
                if len(data) == 0:
                    log.debug("cell (%d,%d): null (field %s) is expected to be a  Numeric" %(jd+2, i+1, playground.dataHeaderList[DoubleTypeIndex[i]]))
                else:
                    log.debug("cell (%d,%d): %s (field %s) is expected to be a  Numeric"   %(jd+2, i+1, data, playground.dataHeaderList[DoubleTypeIndex[i]]))
    
# def validate_numericType()

def main(csv_filename, schema_uri, version_string):
    global playground
    log.debug("action is about to start")
    
    load_schema(schema_uri, version_string)
    load_csv(csv_filename)
    playground.display()
    
    log.debug("start checking existence")
    validate_existence()
    validate_numericType()
    playground.report()
    
# def main(csv_filename, schema_uri, version_string)

if __name__ == '__main__':
    csv_filename = sys.argv[1]
    schema_uri   = sys.argv[2]
    version_string = sys.argv[3]
    
    main(csv_filename, schema_uri, version_string)
    log.debug("done")
