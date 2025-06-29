import asyncio
import Messanger.Messanger as messanger
import Finder.Finder as finder

async def main():
    await asyncio.gather(
        finder.start_bot(),
        messanger.run_bot()
    )

if __name__ == '__main__':
    asyncio.run(main())