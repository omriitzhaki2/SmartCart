# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# import csv
#
# def main():
#     # Example usage
#     query = "coffee"
#     title, trend_data = scrape_google_trends(query)
#
#     if title and trend_data:
#         print("Title:", title)
#         print("Trend data:", trend_data[:10])  # Print the first 10 data points
#         save_to_csv(title, trend_data, 'google_trends_data.csv')
#         print("Data saved to google_trends_data.csv")
#     else:
#         print("Failed to retrieve data from Google Trends")
#
#     # products_path = 'data/products.csv'
#     # departments_path = 'data/departments.csv'
#     # aisles_path = 'data/aisles.csv'
#     #
#     # products_df = pd.read_csv(products_path)
#     # departments_df = pd.read_csv(departments_path)
#     # aisles_df = pd.read_csv(aisles_path)
#     #
#     # products_df = pd.merge(products_df, departments_df, on='department_id', how='left')
#     # products_df = pd.merge(products_df, aisles_df, on='aisle_id', how='left')
#     # products_df.to_csv('data/supermarket_products.csv')
#
#
# if __name__ == '__main__':
#     main()

import asyncio
from playwright.async_api import async_playwright

SBR_WS_CDP = 'wss://brd-customer-hl_80709a30-zone-omri:uy11uu820a7y@brd.superproxy.io:9222'


async def run(pw):
    print('Connecting to Scraping Browser...')
    browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    try:
        page = await browser.new_page()
        print('Connected! Navigating to https://trends.google.com/trends/explore?date=all&q=facbook...')
        await page.goto('https://www.indeed.com/career/data-analyst/salaries')
        # CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Scraping Browser's automatic CAPTCHA solver
        # client = await page.context.new_cdp_session(page)
        # print('Waiting captcha to solve...')
        # solve_res = await client.send('Captcha.waitForSolve', {
        #     'detectTimeout': 10000,
        # })
        # print('Captcha solve status:', solve_res['status'])
        print('Navigated! Scraping page content...')
        html = await page.content()
        print(html)
    finally:
        await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == '__main__':
    asyncio.run(main())
