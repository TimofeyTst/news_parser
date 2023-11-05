import asyncio

import aiohttp

from process import Worker


class Client:
    def __init__(self, host, port, task_count, urls_file, debug=False):
        if task_count <= 0:
            raise ValueError("Tasks count must be > 0")

        self.host = host
        self.port = port
        self.task_count = task_count
        self.urls_file = urls_file
        self.debug = debug
        self.que = asyncio.Queue()

        self.sources = ["Yahoo"]
        self.categories = ["Investments"]
        self.supercategories = []
        self.metadata = {
            "texts": [],
            "annotations": [],
        }

        self.processed_urls = 0
        if self.debug:
            self.tasks_created = 0

    def __str__(self):
        return f"Client {self.urls_file=}; {self.task_count=}; {self.top_k=}"

    def start(self):
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.run_tasks())
        except KeyboardInterrupt:
            pass
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    async def run_tasks(self):
        async with aiohttp.ClientSession() as session:
            # Создание асинхронных задач
            workers = [Worker(self, session).start() for _ in range(self.task_count)]
            if self.debug:
                self.tasks_created = len(workers)
                print(f"\033[33mTasks created: {self.tasks_created}\033[0m")

            for data in self.get_data():
                await self.que.put(data)

            await self.que.put(None)
            await asyncio.gather(*workers)

    def get_data(self):
        with open(self.urls_file, "r") as file:
            for data in file:
                yield data.split()

    def get_metadata(self):
        sources = [{"id": idx, "name": name} for idx, name in enumerate(self.sources)]
        categories = [
            {"id": idx, "name": name} for idx, name in enumerate(self.categories)
        ]
        supercategories = [
            {"id": idx, "name": name} for idx, name in enumerate(self.supercategories)
        ]

        metadata = {
            "sources": sources,
            "categories": categories,
            "supercategories": supercategories,
            "texts": self.metadata["texts"],
            "annotations": self.metadata["annotations"],
        }
        return metadata
