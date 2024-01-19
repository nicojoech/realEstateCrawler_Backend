## Parameters for Testing

1. Crawling interval in seconds 
=> *scheduler.py* => line 79 & 82
2. Duration unit of the crawling process
=> *scheduler.py* => line 113
3. Scheduler Initialization
=> *crudAgent.py* => line 71 to 79
   - (optional) crawl_all can be set to true to crawl all results
	
#### Example of Scheduler Initialization: 
##### interval_hours=1, duration_hours=10 & receiver_email=test@test.com
    --> Crawler Interval = 120 sec (depending on scheduler.py)
    --> Duration = 10 MINUTES (depending on scheduler.py)
