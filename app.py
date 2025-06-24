import asyncio
import Messanger.Messanger as messanger
import Finder.Finder as finder
import Finder.weather_api.weater as w
from utils.logs import Log_Info
import utils.utils as ut

async def main():
    await asyncio.gather(
        finder.start_bot(),
        messanger.run_bot()
    )

if __name__ == '__main__':
    asyncio.run(main())