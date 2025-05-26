import asyncio
import Messanger.main as messanger
import Finder.Finder_bot as finder
import connection.database_con as dt

async def main():
    await dt.start_con()
    await messanger.start_bot()
    await finder.start_bot()

