from pymodbus.client import AsyncModbusSerialClient
import asyncio


async def run():
    client = AsyncModbusSerialClient(port="/dev/ttyS0", baudrate=9600)
    await client.connect()
    while True:
        res = await client.read_coils(slave=2,address=0)
        await client.write_coil(0, res.bits[0], slave=1)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run())
