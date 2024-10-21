import pytest

from src.app import DogsPicturesUploader
from src.framework.http_api import DogsApi, YaUploader


@pytest.mark.parametrize('breed', ['doberman', 'bulldog', 'collie'])
def test_proverka_upload_dog(
    yandex_http_client: YaUploader,
    dogs_api_client: DogsApi,
    application: DogsPicturesUploader,
    breed
):
    # загружаем картинку:
    application.upload_breed_image(breed)

    # проверка: получаем содержимое директории на Яндекс.диске
    expected_name = "test_folder"
    response = yandex_http_client.get_contents(expected_name)

    # проверяем характеристики полученного от Яндекса ответа:
    assert (type_ := response["type"]) == "dir", f"Ожидалась директория, получено {type_}"
    assert (actual_name := response["name"]) == "test_folder", f"Название директории должно быть {expected_name}, получено {actual_name}"

    # проверяем набор элементов в ответе:
    response_items_list = response["_embedded"]["items"]
    if (breeds_list := dogs_api_client.get_sub_breeds_list(breed)) == []:
        assert len(response_items_list) == 1, "Количество элементов не соответствует ожидаемому"
    else:
        assert len(response_items_list) == len(breeds_list), "Количество элементов не соответствует ожидаемому"
    for item in response_items_list:
        assert (type_ := item["type"]) == "file", f"Тип одного из элементов оказался не файл, а {type_}"
        assert (name := item["name"]).startswith(breed), f"Название элемента '{name}' не начинается с названия породы"
