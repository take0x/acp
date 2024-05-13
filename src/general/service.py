import time
from logging import getLogger

import requests
import requests.cookies
from bs4 import BeautifulSoup

from src.general.utils import HttpStatusCode

logger = getLogger(__name__)


class WebService:
    class URLs:
        pass

    class Exceptions:
        class AccessError(Exception):
            pass

        class LoginFailedError(Exception):
            pass

        class ProblemsNotFoundError(Exception):
            pass

    def __init__(self, parser: str = "lxml") -> None:
        self._session: requests.Session = requests.Session()
        self._response: requests.Response | None = None
        self._soup: BeautifulSoup | None = None
        self.parser = parser

    def wait(self, seconds: float) -> None:
        time.sleep(seconds)

    @property
    def session(self) -> requests.Session:
        return self._session

    @property
    def is_logged_in(self) -> bool:
        return False

    @property
    def response(self) -> requests.Response:
        return self._response if self._response else requests.Response()

    @property
    def soup(self) -> BeautifulSoup:
        return self._soup if self._soup else BeautifulSoup()

    def get(self, url: str, *args: tuple, **kwargs: dict) -> BeautifulSoup:
        logger.info("GET: %s", url)
        self._response = self._session.get(url, *args, **kwargs)
        if self.response.status_code != HttpStatusCode.OK.value:
            msg = f"Failed to get {url}. Status code: {self.response.status_code}"
            raise self.Exceptions.AccessError(msg)
        self._soup = BeautifulSoup(self.response.text, self.parser)
        return self.soup

    def post(self, url: str, *args: tuple, **kwargs: dict) -> BeautifulSoup:
        logger.info("POST: %s", url)
        self._response = self._session.post(url, *args, **kwargs)
        if self.response.status_code != HttpStatusCode.OK.value:
            msg = f"Failed to post {url}. Status code: {self.response.status_code}"
            raise self.Exceptions.AccessError(msg)
        self._soup = BeautifulSoup(self.response.text, self.parser)
        return self.soup

    def login(self, data: dict) -> None:
        pass

    @property
    def cookies(self) -> requests.cookies.RequestsCookieJar:
        return self._session.cookies