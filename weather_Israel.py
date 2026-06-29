from mcp.server.fastmcp import FastMCP
import playwright
from playwright.async_api import TimeoutError as PlaywrightTimeout
from playwright.async_api import async_playwright


mcp = FastMCP("weather-Israel")

FORECAST_URL = "https://www.weather2day.co.il/forecast"

myplaywright = None
browser = None
page = None


@mcp.tool()
async def open_weather_forecast_israel() -> str:
    #הפונקציה פותחת את הדפדפן ומנווטת לדף של אתר מזג האויר.
    """Open the weather forecast page"""
    global myplaywright, browser, page
    myplaywright = await async_playwright().start()
    browser = await myplaywright.chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto(FORECAST_URL)
        
    print("Opening browser...")
    return "Weather forecast page opened successfully."

@mcp.tool()
async def enter_weather_forecast_city_israel(city: str) -> str:
    #הפונקציה מכניסה את שם העיר לדף של אתר מזג האויר.
    """Enter the city for weather forecast"""
    global page

    await page.fill("#city_search_forecast", city)
    return f"City {city} entered successfully."
    
@mcp.tool()
async def select_weather_forecast_city_israel() -> str:
    #הפונקציה בוחרת את העיר שהוזנה ומציגה את תחזית מזג האויר.
    """Select the city for weather forecast"""
    global page

    await page.wait_for_selector("#city_search_forecastautocomplete-list")

    await page.locator("#city_search_forecastautocomplete-list div").first.click()
    return "City selected successfully."


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
