# --------------------------------------------------------------------------------------------------------
# 2020/07/18
# src - control_facade.py
# md
# --------------------------------------------------------------------------------------------------------
from datetime import datetime, timedelta

"""
Config: Reads the configuration
Control: Sets the configuration
"""

conf_all = {
    # Twitter
    'scrape_profiles': True,
    'scrape_tweets': True,
    'scrape_only_missing_dates': False,
    'scrape_with_proxy': True,
    'end_date': datetime.today(),
    'begin_date': datetime.now() - timedelta(days=1),
    'time_delta': 360,
    'max_n_fails': 10,
    # Proxies
    'scrape_proxies': True,
    'proxies_download_sites': {'free_proxy_list': False, 'hide_my_name': False},
    # System
    'database': 'twitter_database',
    'logging_level': 'Debug',
}

conf = conf_all


class _Config:

    def __init__(self):
        self._config = conf  # set it to conf

    def get_property(self, property_name):
        if property_name not in self._config.keys():
            return None
        return self._config[property_name]


class Scraping_cfg(_Config):

    @property
    def proxies(self):
        return self.get_property('scrape_proxies')
    @property
    def proxies_download_sites(self):
        return self.get_property('proxies_download_sites')

    @property
    def profiles(self):
        return self.get_property('scrape_profiles')

    @property
    def tweets(self):
        return self.get_property('scrape_tweets')

    @property
    def missing_dates(self):
        return self.get_property('scrape_only_missing_dates')

    @property
    def use_proxy(self):
        return self.get_property('scrape_with_proxy')

    @property
    def begin(self):
        return self.get_property('begin_date')

    @property
    def end(self):
        return self.get_property('end_date')

    @property
    def time_delta(self):
        return self.get_property('time_delta')

    @property
    def max_n_fails(self):
        return self.get_property('max_n_fails')


class SystemCfg(_Config):

    @property
    def database(self):
        return self.get_property('database')

    @property
    def logging_level(self):
        return self.get_property('logging_level')


if __name__ == '__main__':
    s_cfg = Scraping_cfg()
    x = s_cfg.end
    print(x)

    xx = SystemCfg()
    print(xx.logging_level)
