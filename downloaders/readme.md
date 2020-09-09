#this script downloads daily price data for US equitys and mixes with fundamentals data
this is a work in progress and a very crappy thrown together version 

calling the script 'get_it.py'
will promt 'which security y'ont?:'
enter a ticker symbol and if it can find both fundamentals and price data, out pops a csv file with
them mixed together, in the directory 'data'

my goal for this is to make it into a library that can be called in jupyter notebooks to simplify scraping/gathering fundamentals, intraday, and daily data and mix it together.
