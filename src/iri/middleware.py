"""
"""
from typing import List, Dict, Callable, Any

from exception import MiddlewareError


class Compose:
    """
    """

    def __init__(self, middlewares: List[Callable[[Dict[str, Any]], Any]]):
        self._middlewares = middlewares

    def __call__(self, event: Dict[str, Any]):
        try:
            return [m(event) for m in self._middlewares]
        except Exception as e:
            raise MiddlewareError(e)


class PathParam:

    def __init__(self, key: str):
        self._key = key

    def __call__(self, event: Dict[str, Any]):
        return event.get("pathParameters", {}).get(self.key)

    @property
    def key(self):
        return self._key
