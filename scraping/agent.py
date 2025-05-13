from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv
import os


# read gemini api key 
load_dotenv()

import asyncio

# pick gemini

llm = ChatGoogleGenerativeAI(
    model='gemini-2.0-flash-exp',
    google_api_key=os.environ["GEMINI_API_KEY"]
)

# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        # Specify the path to your Chrome executable
        # browser_binary_path="C:\Program Files\Google\Chrome\Application\chrome.exe"
        # For Windows, typically: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        # For Linux, typically: '/usr/bin/google-chrome'
    )
)

async def main():
    agent = Agent(
        task="Find a graphics card on Newegg. Simply search up 'rtx 5070' on the site (type 'rtx 5070' into the task bar at the top, then hit the search button. this should yield many results). Report the first graphics card you find that matches the description.",
        llm=llm,
        browser=browser
    )
    result = await agent.run()
    print(result)
    await browser.close()

asyncio.run(main())