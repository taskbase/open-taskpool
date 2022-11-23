ARG BASE_IMAGE
FROM $BASE_IMAGE

COPY taskpool/server /taskpool/server
# For unit-testing
COPY taskpool/pytest.ini /taskpool/pytest.ini
COPY taskpool/test.db /taskpool/test.db

RUN pip install -q --no-cache-dir --upgrade -r server/requirements.txt && \
    apt -u update && \
    apt -y upgrade && \
    rm -rf /var/lib/apt/lists/* \

RUN [ ! -f /taskpool.db ] && cp /taskpool/docker/local-dev-env/empty.db /taskpool/taskpool.db || true

EXPOSE 58000

CMD ["PYTHONPATH=/taskpool/server/src", "uvicorn", "main:taskpool_app", "--host", "0.0.0.0", "--port", "58000"]
