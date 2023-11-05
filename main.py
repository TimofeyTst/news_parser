import argparse

from async_client import Client
import time
import json


def save_to_json(content, filename="about.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(content, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    start = time.time()

    parser = argparse.ArgumentParser(description="Client for Master-Worker Server")
    parser.add_argument("urls_file", help="File containing URLs")
    parser.add_argument(
        "-c", "--task_count", default=5, type=int, help="Count of asynchronous requests"
    )
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=8080, help="Server port")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    client = Client(
        args.host,
        args.port,
        args.task_count,
        args.urls_file,
        debug=args.debug,
    )
    client.start()

    save_to_json(client.get_metadata(), "data/about.json")
    end = time.time()
    print(f"Time: {end - start} seconds")
