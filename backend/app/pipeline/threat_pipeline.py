import time

class ThreatPipeline:

    def run(self):
        """
        Executes the complete intelligence pipeline.

        Responsibilities

        1. Collect intelligence
        2. Normalize intelligence
        3. Merge intelligence
        4. Return merged threats

        Does NOT

        • Enrich
        • Store
        """

        raise NotImplementedError


pipeline = ThreatPipeline()
