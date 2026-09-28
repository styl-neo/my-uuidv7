from random import getrandbits
from time import time_ns
import logging
import logging.handlers

logger: logging.Logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.handlers.clear()
formatter: logging.Formatter = logging.Formatter("{asctime} | {name:^11} | {levelname:^9s} | {message}", style='{')

str_handler: logging.Handler = logging.StreamHandler()
str_handler.setFormatter(formatter)
# logger.addHandler(str_handler)

file_handler: logging.Handler = logging.handlers.RotatingFileHandler(
    filename="log.log",
    backupCount=1,
    maxBytes=10*1024,
    mode='a'
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def to_hexstr(uuid: int) -> str:
    s: str = uuid.to_bytes(16, byteorder='big').hex()
    return s[:8] + "-" + s[8:12] + "-" + s[12:16] + "-" + s[16:20] + "-" + s[20:]

def gen_uuidv7() -> int:

    # unix_ts_ms - 48 bits
    ts_ms: int = time_ns() // 1_000_000
    ts_ms = ts_ms & 0xFFFF_FFFF_FFFF

    # ver - 4 bits
    ver: int = 0x7

    # rand_a - 12 bits
    rand_a: int = getrandbits(12)

    # var - 2 bits
    var: int = 0b10

    # rand_b - 12 bits
    rand_b: int = getrandbits(62)

    logger.debug(f"time_ts\t{ts_ms.to_bytes(6, byteorder='big').hex()}")
    logger.debug(f"ver \t{ver.to_bytes().hex()}")
    logger.debug(f"rand_a\t{rand_a.to_bytes(2, byteorder='big').hex()}")
    logger.debug(f"var \t{var.to_bytes().hex()}")
    logger.debug(f"rand_b\t{rand_b.to_bytes(8, byteorder='big').hex()}")

    uuid: int = (ts_ms << 80) | (ver << 76) | (rand_a << 64) | (var << 62) | rand_b

    logger.debug(f"final\t{uuid.to_bytes(16, byteorder='big').hex()}")

    return uuid

def main():
    u = gen_uuidv7()
    uuid = to_hexstr(u)
    logger.info(uuid)

if __name__ == "__main__":
    main()
