from datetime import datetime, timedelta
import os
import asyncio
import re
from typing import List

import httpx
from httpx import Response
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")

options = {"x-api-key": API_KEY}

end_date = datetime.now()
start_date = end_date - timedelta(days=7)

date_range_start = start_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
date_range_end = end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

report_options = {
    "dateRangeStart": date_range_start,
    "dateRangeEnd": date_range_end,
    "summaryFilter": {
        "groups": ["DATE"]
    }
}

TASKS_URL = f"https://api.clockify.me/api/v1/workspaces/{WORKSPACE_ID}/projects/{PROJECT_ID}/tasks"
REPORT_URL = f"https://reports.api.clockify.me/v1/workspaces/{WORKSPACE_ID}/reports/summary"


async def get_response_from_url(url: str, headers: dict) -> Response:
    async with httpx.AsyncClient(headers=headers) as client:
        return await client.get(url)


async def make_post_request(url: str, data: dict, headers: dict) -> httpx.Response:
    async with httpx.AsyncClient(headers=headers) as client:
        return await client.post(url, json=data)


def iso_to_seconds(time_str: str) -> int:
    if not time_str:
        return 0

    match = re.findall(r'(\d+)M(\d+)S', time_str)
    if match:
        minutes, seconds = map(int, match[0])
        total_seconds = minutes * 60 + seconds
        return total_seconds
    else:
        return 0


def get_tasks_duration(tasks: List[dict]) -> dict:
    result = {}
    for task in tasks:
        result[task.get('name')] = task.get('duration')

    return result


async def fetch_and_process_data():
    try:
        res = await get_response_from_url(TASKS_URL, options)
        tasks = res.json()
        durations = {k: iso_to_seconds(v) for k, v in get_tasks_duration(tasks).items()}
        return durations
    except Exception as e:
        raise RuntimeError(f"Error fetching and processing data: {e}")


async def main():
    try:
        print("Fetching and processing task data...")
        durations = await fetch_and_process_data()
        print("\nTask Durations:")
        for task, duration in durations.items():
            print(f"{task}: {duration} seconds")

        print("\nFetching and processing report data...")
        post = await make_post_request(REPORT_URL, headers=options, data=report_options)
        report_data = post.json()
        durations = get_tasks_duration(report_data.get("groupOne"))
        print("\nReport Task Durations:")
        for task, duration in durations.items():
            print(f"{task}: {duration} seconds")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
