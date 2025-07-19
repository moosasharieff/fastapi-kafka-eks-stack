import asyncio
import random
from aiohttp import ClientSession
from faker import Faker

# Initialize Faker for generating random data
fake = Faker()

# URL of your FastAPI endpoint
url = "http://localhost:8000/order"


# Function to generate random data
def generate_random_data():
    item = fake.word()  # Random word for the item
    quantity = random.randint(1, 10)  # Random quantity between 1 and 10
    return {"item": item, "quantity": quantity}


# Function to send POST request with random data using aiohttp
async def send_data_to_api(session: ClientSession):
    data = generate_random_data()
    try:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                print(f"Data sent successfully: {data}")
            else:
                print(f"Failed to send data: {data} - Status Code: {response.status}")
    except Exception as e:
        print(f"Request failed: {e}")


# Function to simulate continuous data pushing with multiple workers
async def push_data_continuously(num_workers=10, interval=1):
    async with ClientSession() as session:
        while True:
            tasks = [send_data_to_api(session) for _ in range(num_workers)]
            await asyncio.gather(*tasks)
            print(
                f"Data pushed with {num_workers} workers. Waiting {interval} seconds before next push."
            )
            await asyncio.sleep(interval)


# Start the service
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        push_data_continuously(num_workers=10, interval=2)
    )  # Send data with 10 workers every 2 seconds
