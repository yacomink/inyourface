class CacheProviderForTests(object):

    should_cache = False
    cache = {}
    get_calls = {}
    set_calls = {}

    def __init__(self, should_cache=False):
        self.get_calls = {}
        self.set_calls = {}
        self.cache = {}
        self.should_cache = should_cache

    def get(self, key):
        if (key in self.get_calls):
            self.get_calls[key] = self.get_calls[key] + 1
        else:
            self.get_calls[key] = 1

        if (self.should_cache and key in self.cache):
            return self.cache[key]

        return None

    def set(self, key, value):
        self.set_calls[key] = value
        if (self.should_cache):
            self.cache[key] = value

    def close(self):
        self.cache = {}