from aiohttp import web


async def signin(request):
    data = await request.post()
    pool = request.app["pool"]
    try:
        async with pool.acquire() as conn:
            values = await conn.fetch(
                "select * from test where app = {};".format(data["usr"])
            )
            if len(values) == 0 or values[0]["pass"] != data["pass"]:
                raise Exception
    except:
        return web.Response(text="login failed")
    return web.Response(text="ok")


async def signup(request):
    pool = request.app["pool"]
    data = await request.post()
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                "insert into test values ({},'{}');".format(data["usr"], data["pass"])
            )
    except asyncpg.exceptions.UniqueViolationError:
        return web.Response(text="Already exist")
    return web.Response(text="Insert Ok. User Created.")

