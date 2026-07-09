class CollectorRegistry:

    def __init__(self):
        self.collectors = {}

    def register(self, name, collector):
        print(f"Registering collector: {name}")
        self.collectors[name] = collector

    def get(self, name):
        return self.collectors[name]

    def list(self):
        return list(self.collectors.keys())


collector_registry = CollectorRegistry()

from app.collectors import nvd_collector