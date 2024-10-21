import requests


class BaseApi:
    def __init__(self, base_url: str):
        self.base_url = base_url.lower().rstrip('/')

    def _urljoin(self, endpoint: str) -> str:
        """
        Для соединения базового урла и эндпойнта независимо от наличия слешей в том и другом.
        urllib.parse.urljoin не используется сознательно - он ведёт себя по-разному при наличии/отсутствии слеша в конце левой части урла,
        поэтому более предсказуемым является собственное решение.

        """
        return f"{self.base_url}/{endpoint.lstrip('/')}"


class YaUploader(BaseApi):
    def __init__(self, base_url: str, token: str):
        super().__init__(base_url)
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {token}'}

    def create_folder(self, path: str):
        """
        Создание директории на Яндекс.диске по указанному пути.

        :param path: путь, по поторому будет создана директория.

        """
        requests.put(self.base_url, headers=self.headers, params={"path": path})

    def upload_files(self, path: str, file_url: str, name: str):
        """
        Загрузка файлов на Яндекс.диск.

        :param path: путь до директории, куда будет загружен файл.
        :param file_url: URL, по которому загруженный файл будет доступен.
        :param name: имя загружаемого файла.

        """
        params = {"path": f'/{path}/{name}', 'url': file_url, "overwrite": True}
        requests.post(self._urljoin("upload"), headers=self.headers, params=params)

    def get_contents(self, path: str) -> dict:
        """
        Получение содержимого указанной директории.

        :param path: путь до директории.
        :return: содержимое указанной директории.
        """
        return requests.get(self.base_url, headers=self.headers, params={"path": path}).json()


class DogsApi(BaseApi):
    def get_sub_breeds_list(self, breed: str) -> list[str]:
        """
        Получить полный список подвидов породы.

        :param breed: порода, список подвидов которой будет возвращён. Если такой породы нет, список будет пуст.

        """
        res = requests.get(self._urljoin(f'breed/{breed}/list'))
        return res.json().get("message", [])

    def get_random_breed(self, breed):
        """
        Получить ссылку на случайную картинку указанной породы.

        :param breed: порода.
        :return: ссылка на картинку либо пустая строка, если ничего не найдено.

        """
        res = requests.get(self._urljoin(f"breed/{breed}/images/random"))
        return res.json().get("message", "")

    def get_random_sub_breed(self, breed: str, sub_breed: str) -> str:
        """
        Получить ссылку на случайную картинку подвида указанной породы.

        :param breed: порода.
        :param sub_breed: подвид.
        :return: ссылка на картинку либо пустая строка, если ничего не найдено.

        """
        res = requests.get(self._urljoin(f"breed/{breed}/{sub_breed}/images/random"))
        return res.json().get("message", "")
