import graphene
from datetime import datetime
import asyncio


class SubscriptionExample(graphene.ObjectType):
    time_of_day = graphene.String()

    async def subscribe_time_of_day(root, info):
        while True:
            yield datetime.now().isoformat()
            await asyncio.sleep(1)
