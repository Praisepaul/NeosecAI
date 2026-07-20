import asyncio
import httpx


class GitHubCollector:

    def __init__(self):
        pass

    async def fetch(self, client, cve, semaphore):

        async with semaphore:

            response = await client.get(
                f"https://api.github.com/advisories", params={"cve": cve}
            )

            response.raise_for_status()

            return cve, response.json()

    async def collect_async(self, cves):

        # Create the semaphore inside this event loop
        semaphore = asyncio.Semaphore(10)

        async with httpx.AsyncClient(timeout=60) as client:

            tasks = [self.fetch(client, cve, semaphore) for cve in cves]

            results = await asyncio.gather(*tasks, return_exceptions=False)

        return dict(results)

    def collect(self, cves):

        return asyncio.run(self.collect_async(cves))


collector = GitHubCollector()
