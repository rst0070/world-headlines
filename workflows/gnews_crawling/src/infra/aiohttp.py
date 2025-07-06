import aiohttp
import random


_SESSIONS = []


def get_session(max_num: int = 5) -> aiohttp.ClientSession:
    if len(_SESSIONS) <= max_num:
        _SESSIONS.extend([aiohttp.ClientSession() for _ in range(max_num - len(_SESSIONS))])

    return _SESSIONS[random.randint(0, len(_SESSIONS) - 1)]


async def shutdown_sessions():
    for session in _SESSIONS:
        await session.close()
