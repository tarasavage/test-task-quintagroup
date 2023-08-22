import os
import asyncio
from typing import List

import httpx
from httpx import Response
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.clockify.me/api/v1"
PROJECT_ID = os.getenv("PROJECT_ID")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")

options = {"x-api-key": API_KEY}
TASKS_URL = f"{BASE_URL}/workspaces/{WORKSPACE_ID}/projects/{PROJECT_ID}/tasks"


async def get_response_from_url(url: str, headers: dict) -> Response:
    async with httpx.AsyncClient(headers=headers) as client:
        return await client.get(url)


def extract_task_names(response: Response) -> List:
    if response.status_code == 200:
        tasks = response.json()
        task_names = [task.get("name", "No Name") for task in tasks]
        return task_names
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []


async def main():
    response = await get_response_from_url(TASKS_URL, options)
    print(extract_task_names(response))


if __name__ == "__main__":
    asyncio.run(main())
