# async_test.py
import asyncio
from playwright.async_api import async_playwright, Error as PlaywrightError

async def main():
    print("Starting async Playwright test...")
    
    try:
        async with async_playwright() as pw:
            print("Playwright started successfully!")

            browser = await pw.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--no-zygote",
                    "--single-process",  # helps in some broken Docker envs
                ]
            )
            print("Chromium launched!")

            page = await browser.new_page()
            await page.goto("https://httpbin.org/headers", timeout=30000)
            title = await page.title()
            print(f"Page title = '{title}'")

            await browser.close()
            print("Async test PASSED – everything works!")

    except PlaywrightError as e:
        print(f"Playwright error: {e}")
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

# Run it
if __name__ == "__main__":
    asyncio.run(main())
