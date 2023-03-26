#!/usr/bin/env python3

import os
import re
import requests
import logging
import sys
from typing import Union
from dotenv import load_dotenv   

load_dotenv()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
DEFAULT_URL = "https://www.omdbapi.com/{0}={1}&apikey={2}"

class OMDBAPI:
    def __init__(self) -> None:
        self._api_key = os.getenv('APIKEY')

    def _retrive_url(self, url: str) -> Union[dict, None]:
        r = requests.get(url, timeout=5)
        logging.info("Status code: %s", str(r.status_code))        

        if r.status_code == 200:
            return r.json()
        
        return None


    def search_title(self, title: str) -> None:
        title_format = re.sub(r'\s+', '+', title)
        url = DEFAULT_URL.format("?s", title_format, self._api_key)
        
        response = self._retrive_url(url)
        results = response.get('Search', None)
        if results:
            for result in results:
                logging.info(result)

    def search_imdb_id(self, imdb_id: str, is_full: bool = False) -> None:
        url = DEFAULT_URL.format("?i", imdb_id, self._api_key)
        if is_full:
            url += "&plot=full"
        
        response = self._retrive_url(url)
        logging.info(response)


if __name__ == "__main__":
    omdbapi = OMDBAPI()
    # omdbapi.search_movie("John wick")
    omdbapi.search_imdb_id("tt2911666", is_full=True)