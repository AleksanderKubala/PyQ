class CircuitChanges(object):
    """description of class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.added = []
        self.removed = []

    def add_added(self, layer, added):
        self.added.append((layer, added))


    def add_removed(self, layer, removed):
        self.removed.append((layer, removed))


