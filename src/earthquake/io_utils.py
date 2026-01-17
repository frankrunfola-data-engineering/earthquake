""" 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
File:    io_utils.py
Author:  Frank Runfola
Date:    11/1/2025
-------------------------------------------------------------------------------
Description:
  Tiny IO helpers for this project.
-------------------------------------------------------------------------------
Design goals:
  - Keep the project runnable with minimal dependencies.
  - Keep paths and directory creation centralized.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from __future__ import annotations
from reverse_geocoder import search

def get_country_code(lat, lon):
    try:
      result = search((lat, lon), mode=1)  # mode=1 is often most reliable
      return result[0]["cc"]
    except Exception as e:
        print(f"Error reverse geocoding {lat}, {lon}: {e}")
        return 'unknown'