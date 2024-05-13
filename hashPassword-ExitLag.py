import asyncio
import ssl
from random import randint
from hashlib import sha256
import websockets


ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE



email = input("Insert the account's email: ")

password = "38cf4d8080c1a66172c4a91e76b822140f029e10a00e3615be6eb8a0f3331ffd" 


_uri = "wss://ws01.exitlag.com/exitlag_client"



def pb(_bytes, stage):
    if stage == 0:
        logo = "[SENDING]"
    else:
        logo = "[RECEIVING]"
    print("\n" + logo, end=' ')
    for _x in _bytes:
        print(hex(_x), end=', ')





magicbytes = bytearray([0x32, 0xDA, 0x01, 0x1A])


hwid_1 = bytearray([0]) * 64


for x in range(0, 64):
    hwid_1[x] = randint(0x41, 0x41 + 0xd)


resto_hwid = bytearray(
    [0x22, 0x10, 0x42, 0x46, 0x45, 0x42, 0x46, 0x42, 0x46, 0x46, 0x30, 0x30, 0x30, 0x33, 0x30, 0x36, 0x43, 0x33, 0x2A,
     0x02, 0x70, 0x74, 0x3A, 0x06, 0x34, 0x2E, 0x39, 0x35, 0x2E, 0x32, 0x42, 0x1E, 0x57, 0x69, 0x6E, 0x64, 0x6F, 0x77,
     0x73, 0x20, 0x31, 0x30, 0x20, 0x56, 0x65, 0x72, 0x73, 0x69, 0x6F, 0x6E, 0x20, 0x32, 0x30, 0x30, 0x39, 0x20, 0x36,
     0x34, 0x2D, 0x62, 0x69, 0x74, 0x4A, 0x10, 0x57, 0x69, 0x6E, 0x64, 0x6F, 0x77, 0x73, 0x20, 0x44, 0x65, 0x66, 0x65,
     0x6E, 0x64, 0x65, 0x72, 0x52, 0x00, 0x58, 0x00, 0x62])
resto_hash = bytearray([0x68, 0x10])
number_request = bytearray([0x01])


hash_email_password = sha256(email.encode() + password.encode()).hexdigest().encode()


split_byte = bytearray([0x40])


big_array = bytearray(magicbytes + split_byte + hwid_1 + resto_hwid + split_byte + hash_email_password + resto_hash + split_byte + number_request)



async def initialize_ws_and_send_request():

    async with websockets.connect(_uri, ssl=ssl_context) as ws:

        pb(big_array, 0)

        await ws.send(big_array)

        response = await ws.recv()

        pb(response, 1)


asyncio.get_event_loop().run_until_complete(initialize_ws_and_send_request())
