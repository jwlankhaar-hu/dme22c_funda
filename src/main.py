"""Main module for the Funda project."""

import argparse
from pathlib import Path

import prices
from settings import settings


def main(base_url, csv_file):
    prices.export_prices(base_url, csv_file)


if __name__ == '__main__': 
    
#   ---> Uncomment the following lines to replace the interface
#   with a command line interface:
    
    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '--dest_file',
    #     type=Path, 
    #     help='The destination file (CSV) of exported prices.',
    #     required=True
    # )
    # args = parser.parse_args()
    # csv_file = args.dest_file
    # base_url = settings.url
    # main(base_url, csv_file)

#   ---> In case of a command line interface, deactivate (comment) the 
#   following lines:
        
    csv_file = settings.prices_file    
    base_url = settings.url
    main(base_url, csv_file)