# Run nosetests for server side functions

## On local VM
Enable python virtual environment    
Change directory to `ckanext-ngds`   
Run `. test.sh`   

## With Roberto's Jenkins environment
Modify Line 23-25 in `test-core.ini`   
Enable python virtual environment   
Change directory to `ckanext-ngds`    
Run `nosetests --ckan --with-pylons=test-core.ini`    
