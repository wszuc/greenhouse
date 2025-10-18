import asyncio
import aiohttp

BASE_URL = "http://127.0.0.1:8000"  
TEMP_HYSTERESIS = 1
TEMP_UPPER_HEATER = 55
TEMP_BOTTOM_HEATER = 50


async def get_last_desired_climate(session):
    async with session.get(f"{BASE_URL}/climate/get-climate") as response:
        data = await response.json()
        return data["temperature"]  

async def get_current_temperature(session):
    async with session.get(f"{BASE_URL}/sensors/read/") as response:
        data = await response.json()
        return data[0]

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
        IS_HEATER_COLLING_DOWN = False
        while True:
            try:
                greenhouse_parameters_current = await get_current_temperature(session)
                current_temp = greenhouse_parameters_current["temp_2"]
                heater_temp = greenhouse_parameters_current["temp_3"]
                desired_temp = await get_last_desired_climate(session)

                print(f"Aktualna: {current_temp}°C, Zadana: {desired_temp}°C, Grzałki: {heater_temp}")

                if current_temp < desired_temp - TEMP_HYSTERESIS:
                    # ogrzewamy
                    print("Za zimno – włączanie grzałki, zamknięcie dachu")
                    await roof_close(session)
                    # ogrzewanie po schłodzeniu albo początkowe
                    if heater_temp < TEMP_UPPER_HEATER and not IS_HEATER_COLLING_DOWN:
                        await heating_on(session)
                    # grzałka osiągnęła górną granicę: cooldown
                    elif heater_temp >= TEMP_UPPER_HEATER:
                        IS_HEATER_COLLING_DOWN = True
                        await heating_off(session)
                    elif IS_HEATER_COLLING_DOWN and heater_temp < TEMP_BOTTOM_HEATER:
                        IS_HEATER_COLLING_DOWN = False
                        await heating_on(session)

                elif current_temp > desired_temp + TEMP_HYSTERESIS:
                    print("Za ciepło – wyłączenie grzałki, otwieranie dachu")
                    await heating_off(session)
                    await roof_open(session)
                else:
                    print("Temperatura w normie – zamykanie dachu, wyłączanie grzałki")
                    await roof_close(session)
                    await heating_off(session)

                await asyncio.sleep(1)  # krótka przerwa przed kolejnym odczytem
            except Exception as e:
                print(f"Błąd regulatora: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(regulate_temperature())
