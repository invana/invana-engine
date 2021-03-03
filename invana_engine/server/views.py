from starlette.responses import JSONResponse


async def homepage_view(request):
    return JSONResponse({'message': 'Hello world! go to /graphql'})
