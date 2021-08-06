from os import getenv
from dotenv import load_dotenv
from datetime import datetime
import json
import asyncio
import aiopg
from aiohttp import web
from gino import Gino
from asyncpg.exceptions import UniqueViolationError


load_dotenv()

db = Gino()
app = web.Application()
routes = web.RouteTableDef()
db_dsn = getenv("DB")


class BaseModel:

    @classmethod
    async def get_or_404(cls, obj_id):
        instance = await cls.get(obj_id)
        if instance:
            return instance
        raise web.HTTPNotFound(text='данного ID нет в базе')

    @classmethod
    async def create_instance(cls, **kwargs):
        try:
            instance = await cls.create(**kwargs)
        except UniqueViolationError:
            raise web.HTTPBadRequest()
        return instance


class Advertisements(db.Model, BaseModel):

    __tablename__ = 'advertisements'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author,
            'title': self.title,
            'description': self.description,
            'created_at': str(self.created_at),
        }

    def __str__(self):
        return '<Объявление {}>'.format(self.title)

    def __repr__(self):
        return str(self)


async def set_connection():
    return await db.set_bind(db_dsn)


async def disconnect():
    return await db.pop_bind().close()


async def pg_pool(app):
    async with aiopg.create_pool(db_dsn) as pool:
        app['pg_pool'] = pool
        yield
        pool.close()


async def orm_engine(app):
    app['db'] = db
    await set_connection()
    await db.gino.create_all()
    yield
    await disconnect()


class AdvertisementView(web.View):

    async def get(self):
        ad_id = int(self.request.match_info['ad_id'])
        ad = await Advertisements.get_or_404(ad_id)
        return web.json_response(ad.to_dict())

    async def post(self):
        data = await self.request.json()
        ad = await Advertisements.create_instance(**data)
        return web.json_response(ad.to_dict())

    async def delete(self):
        ad_id = int(self.request.match_info['ad_id'])
        instance = await Advertisements.get_or_404(ad_id)
        await instance.delete()
        return web.Response(text=f'{instance} было удалено')


@routes.get('/health')
async def health(request):
    pool = request.app['pg_pool']
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('SELECT 1')
            data = await cursor.fetchall()
            return web.Response(body=json.dumps({'data': data}))


app.cleanup_ctx.append(orm_engine)
app.cleanup_ctx.append(pg_pool)

app.add_routes([
    web.get('/advert/{ad_id}', AdvertisementView),
    web.post('/advert', AdvertisementView),
    web.delete('/advert/{ad_id}', AdvertisementView),
     ])

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
web.run_app(app, port=8088)
