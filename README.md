# SBMonitor
a web monitor that scrapes a website for its info, filters the differences and sends them to a telegram bot.

this bot also uses nordVPN API to assure that you're safe pushing limitless requests
to websites so you can avoid being flagged and blocked. so make sure that you download
nordVPN desktop and log in or delete those lines if your not interested in using nordVPN.

this scraper parses information using BS4. some websites are familiar with this 
parser and will block your attempts. for those occasions I also made a scraper that's 
based on selenium chromedriver (https://github.com/AsafHaim147/WeidianScrape) so make sure to check it out :)

Step by step guide:
1. make sure you have python and pip installed and working on your machine.
2. download the project to your pc using git shell or as a zip and extract it to a local folder
3. install requirements.txt and verify that indeed all the packages are installed. 
4. go to https://core.telegram.org/bots/tutorial and follow the instructions.
5. once you have your chat id and bot api key, put those in config.py
6. choose the website you want to scrape and copy its link to config.py
7. you're ready! but, one last thing, how can you choose exactly what the bot will send on telegram?
   the function GetShoeDict will use BS4 to extract a specific HTML tag, filter the elements you want
   and add them to a dict so they can be later saved on your assets.json file.
   

   
