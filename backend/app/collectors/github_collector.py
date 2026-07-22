import asyncio

import httpx

from app.config.settings import settings
from app.core.logger import logger


class GitHubCollector:

    def _headers(self):

        headers = {"Accept": "application/vnd.github+json"}

        if settings.github_token:
            headers["Authorization"] = f"Bearer {settings.github_token}"

        return headers

    async def fetch(self, client, cve, semaphore):

        async with semaphore:

            response = await client.get(
                "https://api.github.com/advisories",
                params={"cve": cve},
            )

            if response.status_code == 403:

                remaining = response.headers.get("X-RateLimit-Remaining")
                reset = response.headers.get("X-RateLimit-Reset")

                logger.warning(
                    f"[GitHub] 403 on {cve} - rate limited "
                    f"(remaining={remaining}, reset={reset})"
                )

                return cve, None

            response.raise_for_status()

            return cve, response.json()

    async def collect_async(self, cves):

        semaphore = asyncio.Semaphore(10)

        async with httpx.AsyncClient(timeout=60, headers=self._headers()) as client:

            tasks = [self.fetch(client, cve, semaphore) for cve in cves]

            results = await asyncio.gather(*tasks, return_exceptions=False)

        return {cve: data for cve, data in results if data is not None}

    def collect(self, cves):

        if not cves:
            return {}

        return asyncio.run(self.collect_async(cves))


collector = GitHubCollector()
