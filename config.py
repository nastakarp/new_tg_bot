import configparser

class Config:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    @property
    def telegram_token(self):
        return self.config['telegram']['token']

    @property
    def news_api_key(self):
        return self.config['newsapi']['key']