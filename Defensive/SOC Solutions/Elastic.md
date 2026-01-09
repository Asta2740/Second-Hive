## ELK 

Elastic is not ike other SEIM solutions 
Originally it was developed to store big data , search and visualize it

it's a stack of different open source compenents that work together to collect data from any source store it and visualize it in real time

SOC anaylst strated uisng it as Seim

## Components 

A - Elastic Search

Full Text Search and analytics engine for json formatted doucments
APIS can interact with it

B- logstash

this is the praser that takes the data in inputs apply filteration and output the prased data and this output is sent to kibana  and elastic search

C- Beats

The agent that collects data , there are multiple and different ones each one get a specific type of data

D- Kibana 
the web interface that viusalize all of the data and let analyst create their own dashboards and filters


## Kibana Web

in discover tab , what's important is the filters , logs , search cabability , indexer

search uses Kibana Query language , 

Search query that used to ingest all the logs

there are two ways to search

1- Free Text search 
Just Write anything you want and if it was recognized by any filed it will get you back results

2- iled based search

you used the filed to search you got how it works.