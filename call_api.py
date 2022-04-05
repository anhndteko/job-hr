from asyncio.log import logger
from datetime import datetime
from requests import request, Response
from pydantic import AnyUrl


def call_api(url: AnyUrl, token_iam: str = None, x_api_key: str = None, method: str = 'get', timeout: int = 20, **kwargs) -> Response:
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    if token_iam:
        headers['Authorization'] = token_iam
    params = kwargs.get('params')
    data = kwargs.get('data')

    try:

        response = request(method=method, url=url, headers=headers, timeout=timeout, **kwargs)

        if response.status_code == 200:
            pass
        else:
            logger.error(
                "Calling URL: %s, method: %s, params: %s, data: %s, error code: %s, message: %s" % 
                    (url, method, params, data, response.json().get('code'), response.json()))
        if response.status_code // 100 > 2:
            raise Exception

    except Exception as e:

        logger.error(f"Không thể kết nối đến Endpoint: {url}, method: {method}, params: {params}, data: {data}. Exception: {e}")
        print(e)
        raise e
    return response
