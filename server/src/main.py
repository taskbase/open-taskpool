import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from controllers import router

description = '''
Kristian: kristian@taskbase.com | URL: https://www.taskbase.com/contact | License: <a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons</a>

# Introduction

**NOTE**: This document is work-in-progress. Therefore, small changes like re-namings or re-structuring of data may happen before the initial release.

The taskpool is a growing collection of exercises ("tasks"), which can be fetched through this API and graded with the feedback API (https://bitmark-api.taskbase.com/documentation). It can kickstart your language learning project, by having a large number of tasks ready to go from the beginning!

'''

tags_metadata = [
    {
        "name": "Exercise",
        "description": "Endpoints for working with exercises."
    }
]


def initialize():
    app = FastAPI(
        title="Taskpool API",
        version="0.0.1",
        description=description,
        openapi_tags=tags_metadata
    )
    app.include_router(router)
    app.mount("/audio", StaticFiles(directory="audio-generated"), name="audio")
    return app


taskpool_app = initialize()

if __name__ == "__main__":
    uvicorn.run(taskpool_app, host="0.0.0.0", port=58000)
