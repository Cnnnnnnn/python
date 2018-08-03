import orm, asyncio, sys
from models import User, Blog, Comment

'''
def test():
    yield from orm.create_pool(user='admin', password='password', database='awesome')

    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')

    yield from u.save()

for x in test():
    pass
'''

async def test(loop):
    await orm.create_pool(loop=loop,port=3306,user='root',password='password',db='awesome')
    u = User(name='Test2',email='test2@example.com',passwd='1234567878',image='about:blank',id='111')
    await u.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
