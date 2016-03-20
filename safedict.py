class SafeDict(dict):
    def __init__(self):
        dict.__init__(self)
        self.default = None

    def __missing__(self, key):
        return self.default
