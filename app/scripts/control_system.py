import asyncio
import aiohttp

BASE_URL = "http://127.0.0.1:8000"
TEMP_HYSTERESIS = 1
TEMP_UPPER_HEATER = 65
TEMP_BOTTOM_HEATER = 60


async def get_last_desired_climate(session):
    async with session.get(f"{BASE_URL}/climate/get-climate") as response:
        data = await response.json()
        return {
            "temperature": data["temperature"],
            "lighting": data["lighting"]
        }

async def get_current_sensors(session):
    async with session.get(f"{BASE_URL}/sensors/read/") as response:
        data = await response.json()
        return data[0]

async def heating_on(session): await session.post(f"{BASE_URL}/actuators/heating-on")
async def heating_off(session): await session.post(f"{BASE_URL}/actuators/heating-off")
async def roof_open(session): await session.post(f"{BASE_URL}/actuators/roof-open")
async def roof_close(session): await session.post(f"{BASE_URL}/actuators/roof-close")
async def led_set_level(session, brightness: int): await session.post(f"{BASE_URL}/actuators/led-strip-on", json={"brightness": brightness})
async def led_off(session): await session.post(f"{BASE_URL}/actuators/led-strip-off")
async def watering_on(session): await session.post(f"{BASE_URL}/actuators/watering-on")
async def watering_off(session): await session.post(f"{BASE_URL}/actuators/watering-off")
async def atomiser_on(session): await session.post(f"{BASE_URL}/actuators/atomiser-on")
async def atomiser_off(session): await session.post(f"{BASE_URL}/actuators/atomiser-off")


async def regulate_temperature(session):
    IS_HEATER_COLLING_DOWN = False

    while True:
        try:
            sensors = await get_current_sensors(session)
            current_temp = sensors["temp_2"]
            heater_temp = sensors["temp_3"]

            desired = await get_last_desired_climate(session)
            desired_temp = desired["temperature"]

            if any(v is None for v in [current_temp, heater_temp, desired_temp]):
                raise Exception("Missing temperature data")

            print(f"[TEMP] Aktualna: {current_temp}°C | Zadana: {desired_temp}°C | Grzałki: {heater_temp}")

            if current_temp < desired_temp - TEMP_HYSTERESIS:
                await roof_close(session)
                if heater_temp < TEMP_UPPER_HEATER and not IS_HEATER_COLLING_DOWN:
                    await heating_on(session)
                    print("[HEATING] Włączona")
                elif heater_temp >= TEMP_UPPER_HEATER:
                    IS_HEATER_COLLING_DOWN = True
                    await heating_off(session)
                    print("[HEATING] Grzałka chłodzona")
                elif IS_HEATER_COLLING_DOWN and heater_temp < TEMP_BOTTOM_HEATER:
                    IS_HEATER_COLLING_DOWN = False
                    await heating_on(session)
                    print("[HEATING] Schłodzona – ponowne włączenie")

            elif current_temp > desired_temp + TEMP_HYSTERESIS:
                await heating_off(session)
                await roof_open(session)
                print("[HEATING] Za ciepło – wyłączona, dach otwarty")

            else:
                await heating_off(session)
                await roof_close(session)
                print("[HEATING] W normie")

            await asyncio.sleep(1)

        except Exception as e:
            print(f"[ERROR] {e}")
            await asyncio.sleep(5)

async def regulate_lighting(session):
    while True:
        try:
            sensors = await get_current_sensors(session)
            current_light = sensors["lighting"]

            desired = await get_last_desired_climate(session)
            desired_light = desired["lighting"]

            print(f"[LIGHT] Aktualne: {current_light}, Zadane: {desired_light}")

            if current_light < desired_light:
                await led_set_level(session, desired_light)
                print(f"[LIGHT] Za ciemno – ustawiam LED poziom {desired_light}")
            else:
                await led_off(session)
                print("[LIGHT] Wystarczające światło – wyłączam LED")

            await asyncio.sleep(60)

        except Exception as e:
            print(f"[LIGHT ERROR] {e}")
            await asyncio.sleep(5)

async def regulate_air_humidity(session):
    while True:
        try:
            sensors = await get_current_sensors(session)
            current_humidity = sensors["humidity"]

            desired = await get_last_desired_climate(session)
            desired_humidity = desired["air_humidity"]

            if any(v is None for v in [current_humidity, desired_humidity]):
                raise Exception("Missing humidity data")

            print(f"[AIR HUMIDITY] Aktualna: {current_humidity}% | Zadana: {desired_humidity}%")

            if current_humidity < desired_humidity:
                await atomiser_on(session)
                print("[AIR HUMIDITY] Za sucho – atomizer ON")
            elif current_humidity > desired_humidity:
                await atomiser_off(session)
                print("[AIR HUMIDITY] Zbyt wilgotno – atomizer OFF")

            await asyncio.sleep(3)

        except Exception as e:
            print(f"[AIR HUM ERROR] {e}")
            await asyncio.sleep(5)

async def regulate_soil_moisture(session):
    while True:
        try:
            sensors = await get_current_sensors(session)
            current_soil_moisture_raw = sensors["soil_humidity"]
            if current_soil_moisture_raw > 1.5:
                current_soil_moisture = 3
            elif current_soil_moisture_raw <= 1.5:
                current_soil_moisture = 2
            elif current_soil_moisture < 1.2:
                current_soil_moisture = 1

            desired = await get_last_desired_climate(session)
            desired_soil = desired["soil_humidity"]

            if any(v is None for v in [current_soil_moisture, desired_soil]):
                raise Exception("Missing soil moisture data")

            print(f"[SOIL] Aktualna: {current_soil_moisture} | Zadana: {desired_soil}")

            if current_soil_moisture < desired_soil:
                await watering_on(session)
                print("[SOIL] Za sucho – włączam podlewanie na 2s")
            elif current_soil_moisture > desired_soil:
                await watering_off(session)
                print("[SOIL] Wystarczająco wilgotno - nie załączam podlewania")

            await asyncio.sleep(30)

        except Exception as e:
            print(f"[SOIL MOISTURE ERROR] {e}")
            await asyncio.sleep(5)

async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            regulate_temperature(session),
            regulate_lighting(session),
            #regulate_air_humidity(session),
            regulate_soil_moisture(session)
        )

if __name__ == "__main__":
    asyncio.run(main())
