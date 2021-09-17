# Clear Sky

This tool is designed to search for hidden subdomains or roots/seeds hosted in AWS's IP Range

Methodology based on Daehee Park's fantastic [Blog Post](https://www.daehee.com/scan-aws-ip-ssl-certificates/)  
Used to find subdomains or roots/seeds based jhaddix's equally fantastic [Recon Methodology v4.0](https://www.youtube.com/watch?v=p4JgIu1mceI&t=3088s)  

### TL:DR

Step 1: Use masscan to identify all servers in AWS's IP range with common HTTPs ports open  
Step 2: Use tls-scan to pull SSL certificate data from these servers  
Step 3: Use jq to search SSL certificate data for a matching FQDN or search term  
Step 3: Run a full nmap scan on all servers with a matching certificate  

******************************************************************************************************
    I AM NOT RESPONSABLE FOR HOW YOU USE THIS TOOL.  DON'T BE A DICK!                     
******************************************************************************************************

    python3 clearsky.py [-h] [-u | --update] [-r | --rate] -s | --search [SEARCH_TERM]
                Example: python3 clearsky.py -u -r 40000 -s "tesla.com"
------------------------------------------------------------------------------------------------------
|  Short  |    Long    |  Required  |                               Notes                             |
|---------|------------|------------|-----------------------------------------------------------------|
|   -u    |  --update  |     no     |         Perform initial scan to download certificate data       |
|   -r    |  --rate    |     no     |          Set value of masscan --rate flag (Default 40000)       |
|   -s    |  --search  |     yes    |                FQDN, extension, or term to search               |
-------------------------------------------------------------------------------------------------------
