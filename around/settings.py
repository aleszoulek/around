# Scrapy settings for around project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'around'

SPIDER_MODULES = ['around.spiders']
NEWSPIDER_MODULE = 'around.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'around (+http://www.yourdomain.com)'


ITEM_PIPELINES = [
    'around.pipelines.FillCoords',
    'around.pipelines.ElasticSearchSave',
]
