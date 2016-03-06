class widget:
    def __init__(self, area):
        self.area = area
        self.cursor = None

    def draw(self, surface):
        pass

    def get_cursor(self, pos):
        return self.cursor

    def process_event(self, event):
        pass