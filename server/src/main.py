import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from controllers import router

description = '''
Contact: kristian@taskbase.com | <a href="https://creativecommons.org/licenses/by/4.0/"> Creative Commons Attribution 4.0 </a> 

# Introduction

The taskpool is a growing collection of exercises ("tasks"), which can be fetched through this API and graded with the [Bitmark Feedback API](https://bitmark-api.taskbase.com/documentation). 

It can kickstart your language learning project, by having a large number of tasks ready to go from the beginning!

Currently supported are the language learning tasks for:
- UK 🇺🇦 --> DE 🇩🇪
- DE 🇩🇪 --> EN 🇬🇧

The source code is available at [https://github.com/taskbase/open-taskpool](https://github.com/taskbase/open-taskpool).

'''

tags_metadata = [
    {
        "name": "Exercise",
        "description": "Endpoints for working with exercises."
    },
    {
        "name": "Metadata"
    }
]


def initialize():
    app = FastAPI()
    app.include_router(router)
    app.mount("/audio", StaticFiles(directory="audio-generated"), name="audio")

    openapi_schema = get_openapi(
        title="Open Taskpool API",
        version="0.0.2",
        description=description,
        tags=tags_metadata,
        routes=app.routes
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://tb-open-taskpool.s3.eu-central-1.amazonaws.com/open-taskpool.png"
    }

    app.openapi_schema = openapi_schema

    return app


taskpool_app = initialize()

if __name__ == "__main__":
    uvicorn.run(taskpool_app, host="0.0.0.0", port=58000)
