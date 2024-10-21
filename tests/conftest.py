import pytest

from src.app import DogsPicturesUploader
from src.framework.http_api import DogsApi, YaUploader
from src.constants import DOGS_API_BASE_URL, YANDEX_BASE_URL, YANDEX_TOKEN


@pytest.fixture(scope="session")
def application():
    return DogsPicturesUploader()


@pytest.fixture(scope="session")
def yandex_http_client():
    return YaUploader(base_url=YANDEX_BASE_URL, token=YANDEX_TOKEN)


@pytest.fixture(scope="session")
def dogs_api_client():
    return DogsApi(base_url=DOGS_API_BASE_URL)