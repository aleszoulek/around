#!/bin/bash

curl -XDELETE 'http://localhost:9200/around/'

curl -XPUT 'http://localhost:9200/around/'

curl -XPUT 'http://localhost:9200/around/event/_mapping' -d '
{
    "event" : {
        "properties" : {
            "date_from" : {
                "type" : "date",
                "format": "date",
                "store" : "yes"
            },
            "date_to" : {
                "type" : "date",
                "format": "date",
                "store" : "yes"
            },
            "time_from" : {
                "type" : "date",
                "format": "hour_minute_second",
                "store" : "yes"
            },
            "time_to" : {
                "type" : "date",
                "format": "hour_minute_second",
                "store" : "yes"
            },
            "name" : {
                "type" : "string",
                "store" : "yes"
            },
            "venue" : {
                "type" : "string",
                "store" : "yes"
            },
            "source" : {
                "type" : "string",
                "store" : "yes"
            },
            "description" : {
                "type" : "string",
                "store" : "yes"
            },
            "coords" : {
                "type" : "geo_point",
                "lat_lon": "yes",
                "store" : "yes"
            }
        }
    }
}
'
