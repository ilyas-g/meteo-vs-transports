import asyncio
import aiohttp
import socket
from typing import List, Dict

STATION_INFO_URL = (
    "https://velib-metropole-opendata.smoove.pro/"
    "opendata/Velib_Metropole/station_information.json"
)

STATION_STATUS_URL = (
    "https://velib-metropole-opendata.smoove.pro/"
    "opendata/Velib_Metropole/station_status.json"
)

TIMEOUT = aiohttp.ClientTimeout(
    total=15,
    connect=5,
    sock_read=10
)

async def fetch_json(session: aiohttp.ClientSession, url: str) -> Dict:
    async with session.get(url) as resp:
        resp.raise_for_status()
        return await resp.json()

async def get_merged_station_data() -> List[Dict]:
    connector = aiohttp.TCPConnector(family=socket.AF_INET)

    async with aiohttp.ClientSession(
        timeout=TIMEOUT,
        connector=connector,
        headers={"User-Agent": "velib-service/1.0"},
    ) as session:

        info, status = await asyncio.gather(
            fetch_json(session, STATION_INFO_URL),
            fetch_json(session, STATION_STATUS_URL),
        )

    infos = info["data"]["stations"]
    statuses = status["data"]["stations"]
    status_by_id = {s["station_id"]: s for s in statuses}

    return [
        {**station, **status_by_id.get(station["station_id"], {})}
        for station in infos
    ]

# -------------------------------------------------------------------

if __name__ == "__main__":
    stations = asyncio.run(get_merged_station_data())
    print(f"{len(stations)} stations chargées")

    s = stations[0]
    print(
        f"{s['name']} | "
        f"Vélos: {s.get('num_bikes_available')} | "
        f"Électriques: {s.get('num_ebikes_available')}"
    )