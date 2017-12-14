#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import mediacloud, datetime
import logging
import configparser

logging.basicConfig(filename = 'logs.txt', level = logging. INFO)
logger = logging.getLogger(__name__)

class media_cloud:
    
    def get_API_key(self):
        
        logger.info('Getting API key from config file...')
        config = configparser.ConfigParser()
            
        try:
            config.read('../config.ini')
            self.api_key = config['MEDIACLOUD']['api_key']
        except Exception:
            logger.error('Failed to read the file', exo_info = True)
            
    def make_mc_connection(self):
        self.mc_connection = mediacloud.api.media_cloud(self.apo_key)
        if self.mc_connection is None:
            logger.error('Cannot make connection.')
            
    def handle_request(self, search_tuple, start_date, end_date):
        self.get_API_key()
        self.make_mc_connection()
        logger.info('Handling request...')
        logger.info('Search term(s): %s', search_tuple)
        logger.info('Start date: %s', start_date)
        logger.info('End date: %s', end_date)
        result = self.mc_connection.sentenceCount(str(search_tuple), solr_filter=[self.mc_connection.publish_date_query(datetime.date(start_date[0], start_date[1], start_date[2]), datetime.date(end_date[0], end_date[1], end_date[2])) ])
        logger.info('Return result: %s', result)
        return result      

mc = media_cloud()
trump = mc.handle_request(('Trump'), (2016, 9, 1), (2016, 9, 30))
clinton = mc.handle_request(('Clinton'), (2016, 9, 1), (2016, 9, 30))
print(trump['count'])
print(clinton['count'])