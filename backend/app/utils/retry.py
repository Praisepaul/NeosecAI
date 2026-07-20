import time
import httpx


def retry(
    function,
    retries=2,
    delay=2,
):

    for attempt in range(retries + 1):

        try:

            return function()

        except httpx.HTTPStatusError as error:

            status_code = error.response.status_code

            # Do not retry permanent client errors
            if status_code in {400, 401, 403, 404}:

                print(f"[Retry] Non-retryable HTTP error " f"{status_code}: {error}")

                return None

            if attempt == retries:

                print(f"[Retry] Failed after {retries + 1} attempts: " f"{error}")

                return None

            print(f"[Retry] Attempt {attempt + 1} failed: {error}")

            time.sleep(delay)

        except (
            httpx.TimeoutException,
            httpx.NetworkError,
            httpx.ConnectError,
        ) as error:

            if attempt == retries:

                print(
                    f"[Retry] Network failure after " f"{retries + 1} attempts: {error}"
                )

                return None

            print(f"[Retry] Network error. " f"Retrying in {delay} seconds: {error}")

            time.sleep(delay)

    return None
