import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

GITHUB_URL = "https://api.github.com/advisories"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


class GitHubCollector:

    def __init__(self):

        self.semaphore = asyncio.Semaphore(10)
        if not GITHUB_TOKEN:
            print("[GitHub] Warning: No GitHub token configured.")

    async def fetch(self, client, cve):

        async with self.semaphore:

            try:

                response = await client.get(
                GITHUB_URL,
                params={"cve_id": cve},
                headers = {
                    "Accept": "application/vnd.github+json",
                    "Authorization": f"Bearer {GITHUB_TOKEN}",
                    "X-GitHub-Api-Version": "2022-11-28"
                }
                )

                if response.status_code != 200:

                    print(response.text)

                    return cve, None

                advisories = response.json()

                return cve, advisories

            except Exception as e:

                print(f"[GitHub] {cve}: {e}")

                return cve, None

    async def collect_async(self, cves):

        advisories = {}

        limits = httpx.Limits(

            max_connections=20,
            max_keepalive_connections=10

        )

        timeout = httpx.Timeout(60.0)

        async with httpx.AsyncClient(

            timeout=timeout,
            limits=limits

        ) as client:

            tasks = [

                self.fetch(client, cve)

                for cve in cves

            ]

            results = await asyncio.gather(*tasks, return_exceptions=False)

        for cve, data in results:

            if data:

                advisories[cve] = data

        return advisories

    def collect(self, cves):

        return asyncio.run(

            self.collect_async(cves)

        )


collector = GitHubCollector()

from app.jobs.collector_registry import collector_registry

collector_registry.register(
    "github",
    collector
)