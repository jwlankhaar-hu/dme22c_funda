"""Settings module for the Funda project."""

import csv
from pathlib import Path

from pydantic import BaseSettings


class _Settings(BaseSettings):
    """Settings class for the project. To be instantiated once
    only.
    """
    base_dir: Path = Path(__file__).parents[1]
    data_dir: Path = base_dir / 'data'
    
    city: str = 'Maarssen'
    url: str = fr'https://www.funda.nl/koop/{city.lower()}'
    
    request_headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50'
    }
    
    prices_file: Path = data_dir / 'price_list.csv' 
    csv_options: dict = {
        'delimiter': ',', 
        'quotechar': '"', 
        'quoting': csv.QUOTE_ALL
    }


settings = _Settings()

    


    
