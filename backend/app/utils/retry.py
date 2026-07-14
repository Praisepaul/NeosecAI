import time


def retry(function, retries=2, delay=1):

    for attempt in range(retries):

        try:
            return function()

        except Exception as ex:

            print(f"Retry {attempt + 1}/{retries} failed: {ex}")

            if attempt < retries - 1:
                time.sleep(delay)

            else:
                raise
