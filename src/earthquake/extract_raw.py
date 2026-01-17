""" 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
File:    extract_raw.py
Author:  Frank Runfola
Date:    11/1/2025
-------------------------------------------------------------------------------
Description:
  Tiny helpers for this project.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

import requests
import json

def extract_raw(base_url,start_date, end_date)-> str:
    print(f"\n  extract_raw()")
    data = ""
    url = f"{base_url}&starttime={start_date}&endtime={end_date}"
    
    try:
        print(f"    get(url={url})")
        response = requests.get(url)
        response.raise_for_status()
        print(f"    get raw json")
        data = response.json().get('features', [])
        #print(json.dumps(data[:3] if data else [], indent=2))   # Print the first 3 records (pretty)
        #for rec in data[:3]:                                    # Print one record per line (JSONL-style)
        #    print(f"    {json.dumps(rec)}")        
        print("    Row count:", len(data))
        
        if not data:
            print("No data returned for the specified date range.")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    
    return data
