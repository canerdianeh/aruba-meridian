# A collection of scripts for working with the Aruba Meridian API

**beacon-export.py**: Export a list of beacons to CSV
  * Arguments:
  	* *output filename*
  
  * Caveats: 
  	* Excel will mangle any map or location IDs as they are 16-digit numbers. Import manually and specify as text or use another application. 

**pm_export_csv.py**: Export a list of placemarks to CSV
  * Arguments:
  	* *output filename*
  
  * Caveats: 
  	* Excel will mangle any map or location IDs as they are 16-digit numbers. Import manually and specify as text or use another application. 

**pm_import_csv.py**: Import a list of placemarks from CSV - updates existing placemarks and creates new ones. 
  * Arguments:
  	* *output filename*
  
  * Caveats: 
  	* Excel will mangle any map or location IDs as they are 16-digit numbers. Import manually and specify as text or use another application. 

