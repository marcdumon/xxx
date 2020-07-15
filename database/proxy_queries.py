# --------------------------------------------------------------------------------------------------------
# 2020/07/04
# src - proxy_queries.py
# md
# --------------------------------------------------------------------------------------------------------

from pymongo import MongoClient, DESCENDING
from pymongo.errors import DuplicateKeyError

from config import DATABASE
from tools.logger import logger

"""
Group of queries to store and retrief data from the proxies collection.
The queries start with 'q_' 
Queries accept and return a dict or a lists of dicts when suitable

Convention:
-----------
- documnet:     d
- query:        q
- projection:   p
- sort:         s
- filter:       f
- update:       u
- pipeline      pl
- match         m
- group:        g

IMPLEMENTED QUERIES
-------------------
- q_get_proxies(q)
- q_save_a_proxy(proxy)
- q_update_a_proxy_test(proxy_test)
- q_reset_a_proxy_scrape_success_flag(proxy)
- q_set_a_proxy_scrape_success_flag(proxy, scrape_success_flag)
"""

collection_name = 'proxies'


def get_collection():  # Todo: same function in many modules. Put in tools?
    client = MongoClient()
    db = client[DATABASE]
    collection = db[collection_name]
    return collection


def setup_collection():
    collection = get_collection()
    collection.create_index([('ip', DESCENDING), ('port', DESCENDING)], unique=True)


def q_get_proxies(q):  # Todo: remove q here ?
    collection = get_collection()
    p = {'ip': 1, 'port': 1, 'delay': 1, 'blacklisted': 1, '_id': 0}
    cursor = collection.find(q, p)
    proxies = list(cursor)

    return proxies


def q_save_a_proxy(proxy):
    collection = get_collection()
    d = proxy
    # New proxies have not been tested
    d['delay'] = 999999
    d['blacklisted'] = True
    d['error_code'] = 0
    d['test_n_blacklisted'] = 0
    d['test_n_tested'] = 0
    d['scrape_success'] = True
    d['scrape_n_used'] = 0
    d['scrape_n_failed'] = 0
    d['scrape_n_used_total'] = 0
    d['scrape_n_failed_total'] = 0
    try:
        collection.insert_one(d)
    except DuplicateKeyError as e:
        logger.warning(f"Duplicate proxy: {proxy['ip']}:{proxy['port']}")


def q_update_a_proxy_test(proxy_test):
    collection = get_collection()
    f = {'ip': proxy_test['ip'],
         'port': proxy_test['port']}
    u = {'$set': {'delay': proxy_test['delay'],
                  'blacklisted': proxy_test['blacklisted'],
                  'error_code': proxy_test['error_code']},
         '$inc': {'test_n_blacklisted': int(proxy_test['blacklisted']),
                  'test_n_tested': 1}}
    collection.update_one(f, u, upsert=True)


def q_set_a_proxy_scrape_success_flag(proxy, scrape_success_flag):
    collection = get_collection()
    f = {'ip': proxy['ip'], 'port': proxy['port']}
    u = {'$set': {'scrape_success': scrape_success_flag}}
    if scrape_success_flag:
        u['$inc'] = {'scrape_n_used': 1}
        u['$inc'] = {'scrape_n_used_total': 1}
    else:
        u['$inc'] = {'scrape_n_used': 1, 'scrape_n_failed': 1}
        u['$inc'] = {'scrape_n_used_total': 1, 'scrape_n_failed_total': 1}
    collection.update_one(f, u, upsert=True)


def q_reset_a_proxy_scrape_success_flag(proxy):
    collection = get_collection()

    f = {'ip': proxy['ip'], 'port': proxy['port']}
    u = {'$set': {'scrape_success': True}}  # 'n_used': 0, 'n_failed': 0}
    collection.update_one(f, u, upsert=True)


if __name__ == '__main__':
    pass
    # setup_collection()
    # proxy_test = {'ip': '1.1.1.1', 'port': '2332', 'delay': .03, 'blacklisted': False}
    # q_update_a_proxy_test(proxy_test)
    # col =get_collection()
    # for proxy in col.find():
    #     col.update_one({'_id':proxy['_id']},
    #                    {'$set': {'test_n_blacklisted': int(proxy['blacklisted']), 'test_n_tested': 1}})
