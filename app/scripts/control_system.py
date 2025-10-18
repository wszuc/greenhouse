import asyncio
import aiohttp

BASE_URL = "http://127.0.0.1:8000"
TEMP_HYSTERESIS = 1

async def get_current_temperature(session):
    async with session.get(f"{BASE_URL}/sensors/read/") as response:
        data = await response.json()
        return data[0]["temp_2"]  # używamy temp_2 jako głównej temperatury

async def get_desired_temperature(session):
    async with session.get(f"{BASE_URL}/desiredclimate/last") as response:
        data = await response.json()
        return data["temperature"]

async def heating_on(session):
    await session.post(f"{BASE_URL}/actuators/heating-on")

async def heating_off(session):
    await session.post(f"{BASE_URL}/actuators/heating-off")

async def roof_open(session):
    await session.post(f"{BASE_URL}/actuators/roof-open")

async def roof_close(session):
    await session.post(f"{BASE_URL}/actuators/roof-close")

async def regulate_temperature():
    async with aiohttp.ClientSession() as session:
        while True:
            current_temp = await get_current_temperature(session)
            desired_temp = await get_desired_temperature(session)

            print(f"Aktualna: {current_temp}°C, Zadana: {desired_temp}°C")

            if current_temp < desired_temp - TEMP_HYSTERESIS:
                await roof_close(session)
                print("Za zimno – włączanie grzałki")
                await heating_on(session)
                await asyncio.sleep(5)
                await heating_off(session)
                print("Grzałka wyłączona, czekamy 30 sekund")
                await asyncio.sleep(30)
            elif current_temp > desired_temp + TEMP_HYSTERESIS:
                print("Za ciepło – otwieranie dachu")
                await roof_open(session)
            else:
                print("Temperatura w normie – zamykanie dachu")
                await roof_close(session)

            await asyncio.sleep(2)  # mała przerwa przed kolejnym odczytem

if __name__ == "__main__":
    asyncio.run(regulate_temperature())
