from functools import lru_cache

from fastapi import FastAPI, Depends

from api.api import api_router

import config

settings = config.Settings()


app = FastAPI(title=settings.app_name)

app.include_router(api_router)




# # settings object will be created only once; the first time it's called
# @lru_cache
# def get_settings():
#     return config.Settings()

