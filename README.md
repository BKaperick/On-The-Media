# On-The-Media

Built in Python 3.5.  Uses [newsapi](https://newsapi.org) to get the daily trending stories at the Washington Post.  Create an API key and save it in apikey.txt.

The command
    `$python scrape_WaPo.py -r`

fetches the daily trending stories and adds their articles' plaintext to articles/.  Then, the three suggested stories are also added, and this process is repeated until the process is killed.  Once you terminate the process, to resume scraping, call
    `$python scrape_WaPo.py`
