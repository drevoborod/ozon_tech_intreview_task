from src.framework.http_api import DogsApi, YaUploader
from src.constants import DOGS_API_BASE_URL, YANDEX_BASE_URL, YANDEX_TOKEN


class DogsPicturesUploader:
    def __init__(self):
        self.dogs_client = DogsApi(base_url=DOGS_API_BASE_URL)
        self.yandex_client = YaUploader(base_url=YANDEX_BASE_URL, token=YANDEX_TOKEN)

    def get_urls(self, breed, sub_breeds):
        url_images = []
        if sub_breeds:
            for sub_breed in sub_breeds:
                res = self.dogs_client.get_random_sub_breed(breed, sub_breed)
                url_images.append(res)
        else:
            url_images.append(self.dogs_client.get_random_breed(breed))
        return url_images

    def upload_breed_image(self, breed):
        sub_breeds = self.dogs_client.get_sub_breeds_list(breed)
        urls = self.get_urls(breed, sub_breeds)

        self.yandex_client.create_folder('test_folder')
        for url in urls:
            part_name = url.split('/')
            name = '_'.join([part_name[-2], part_name[-1]])
            self.yandex_client.upload_files(path="test_folder", file_url=url, name=name)
