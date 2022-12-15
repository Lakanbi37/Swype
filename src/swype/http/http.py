import httpx

from swype.exceptions import (
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    RequestTimeoutError,
    UpgradeRequiredError,
    TooManyRequestsError,
    ServerError,
    ServiceUnavailableError,
    GatewayTimeoutError,
    UnexpectedError
)
from swype.exceptions.http import InvalidResponseError
from swype.exceptions.http.timeout_error import ConnectTimeoutError, ReadTimeoutError


class Http:

    def __init__(self, secret_key, timeout):
        self._secret_key = secret_key
        self._timeout = timeout
        self._base_url = "https://api.flutterwave.com/v3"

    @staticmethod
    def is_error_status(status):
        return status not in [200, 201]

    @staticmethod
    def raise_exception_from_status(status, message=None):
        if status == 401:
            raise AuthenticationError()
        elif status == 403:
            raise AuthorizationError(message)
        elif status == 404:
            raise NotFoundError()
        elif status == 408:
            raise RequestTimeoutError()
        elif status == 426:
            raise UpgradeRequiredError()
        elif status == 429:
            raise TooManyRequestsError()
        elif status == 500:
            raise ServerError()
        elif status == 503:
            raise ServiceUnavailableError()
        elif status == 504:
            raise GatewayTimeoutError()
        else:
            raise UnexpectedError("Unexpected HTTP_RESPONSE " + str(status))

    @staticmethod
    def handle_exception(exception):
        if isinstance(exception, httpx.ReadTimeout):
            raise ReadTimeoutError(exception)
        elif isinstance(exception, httpx.ConnectTimeout):
            raise ConnectTimeoutError(exception)
        elif isinstance(exception, httpx.ConnectError):
            raise ConnectionError(exception)
        elif isinstance(exception, httpx.HTTPError):
            raise InvalidResponseError(exception)
        elif isinstance(exception, httpx.Timeout):
            raise TimeoutError(exception)
        else:
            raise UnexpectedError(exception)

    class ContentType:
        json = "application/json"
        multipart = "multipart/form-data"

    def _headers(self, content_type):
        headers = {
            "Authorization": f"Bearer {self._secret_key}"
        }
        if content_type == Http.ContentType.json:
            headers["Content-Type"] = Http.ContentType.json
        return headers

    @staticmethod
    def _request_body(params, files):
        if files is None:
            return params
        return params, files

    @staticmethod
    def _request_function(method):
        if method == "GET":
            return httpx.get
        elif method == "POST":
            return httpx.post
        elif method == "PUT":
            return httpx.put
        elif method == "DELETE":
            return httpx.delete

    def _call_api(self, http_verb, path, headers, request_body, query_params=None):
        data = request_body
        files = None
        if query_params is None:
            query_params = {}
        if isinstance(request_body, tuple):
            data = request_body[0]
            files = request_body[1]
        # if type(request_body) is tuple:
        response = self._request_function(http_verb)(
            self._base_url + path,
            headers=headers,
            json=data,
            files=files,
            params=query_params,
            timeout=self._timeout
        )
        return response.status_code, response.json()

    def _make_request(self, http_verb, path, content_type, params=None, files=None, query_params=None):
        response_body = None
        status = None
        headers = self._headers(content_type)
        request_body = self._request_body(params, files)
        full_path = path
        try:
            status, response_body = self._call_api(http_verb, full_path, headers, request_body, query_params)
        except Exception as e:
            self.handle_exception(e)
        print(response_body)
        if Http.is_error_status(status):
            Http.raise_exception_from_status(status)
        else:
            if len(response_body) == 0:
                return {}
            else:
                if content_type == Http.ContentType.json:
                    return request_body

    def post(self, path, params=None):
        return self._make_request("POST", path, Http.ContentType.json, params)

    def delete(self, path):
        return self._make_request("DELETE", path, Http.ContentType.json)

    def get(self, path, params=None):
        return self._make_request("GET", path, Http.ContentType.json, query_params=params)

    def put(self, path, params=None):
        return self._make_request("PUT", path, Http.ContentType.json, params)

    def patch(self, path, params=None):
        return self._make_request("PATCH", path, Http.ContentType.json, params)

    def post_multipart(self, path, files, params=None):
        return self._make_request("POST", path, Http.ContentType.multipart, params, files)
