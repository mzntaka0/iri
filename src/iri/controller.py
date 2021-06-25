"""
"""
from typing import Dict, Any, Literal, List

import middleware
import exception


class APIGatewayLambdaController:
    """

    """
    allow_methods = [
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTION",
    ]

    error_messages = {
        "400": "Bad Request",
        "403": "The http method you throw is out of service in this API. \n Available methods: f{self.allow_methods}",
        "500": "Internal Server Error"
    }

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Method": "GET,POST,PUT,DELETE,OPTIONS",
        "Access-Control-Allow-Origin": "*",
    }

    def __init__(self):
        self.middlewares = middleware.Compose([])

    def __call__(self, event: Dict[str, Any], *args, **kwargs):
        return self.handler(event, *args, **kwargs)

    def __getitem__(self, key):
        return getattr(self, key.lower())

    def handler(self, event: Dict[str, Any], *args, **kwargs):
        if event.get("httpMethod", None) not in self.allow_methods:
            return self.error(
                403,
                "Bad Request"
            )
        http_method: Literal[self.allow_methods] = event["httpMethod"]
        try:
            middleware_input: List[Any] = self.middlewares(event)
            res = self[http_method](event, *middleware_input, *args, **kwargs)
        except exception.MiddlewareError:
            return self.error(
                500,
                self.error_messages["500"]
            )
        except NotImplementedError:
            return self.error(
                400,
                self.error_messages["400"]
            )
        except Exception:
            return self.error(
                500,
                self.error_messages["500"]
            )
        return self.ok(
            200,
            res
        )

    def get(self, event: Dict[str, Any], *args, **kwargs):
        raise NotImplementedError

    def post(self, event: Dict[str, Any], *args, **kwargs):
        raise NotImplementedError

    def put(self, event: Dict[str, Any], *args, **kwargs):
        raise NotImplementedError

    def delete(self, event: Dict[str, Any], *args, **kwargs):
        raise NotImplementedError

    def _override_headers(self, header: Dict[str, Any]):
        for key, val in header.items():
            self.headers[key] = val

    def res(
        self,
        status_code: int,
        body: Any,
        headers: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        return {
            "statusCode": status_code,
            "headers": self._override_headers(headers) if headers else self.headers,
            "body": body
        }

    def ok(self, status_code: int, body: Any) -> Dict[str, Any]:
        return self.res(status_code, body)

    def error(self, status_code: int, msg: str) -> Dict[str, Any]:
        body = {
            "statusCode": status_code,
            "message": msg
        }
        return self.res(status_code, body)
