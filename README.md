# Описание
Тестовое задание на вакансию тестировщика-автоматизатора на Python. 
Ниже представлены задание и решение в соответствующих разделах.

# Задание
### Милые пёсики
У нас есть программа для загрузки [картинок собак](https://dog.ceo/dog-api/documentation). Для этой программы уже написан тест.  
На вход подается порода собаки. Функция находит одну случайную картинку этой собаки и загружает её на [Я.Диск](https://yandex.ru/dev/disk/poligon/).
Если у породы есть подпороды, то для каждой подпороды загружается по одной картинке.
Например, для doberman будет одна картинка, а для spaniel 7 картинок, по одной на каждую подпороду.

### Задание:
Нужно перечислить 10 основных проблем в коде.  
Все найденные проблемы нужно отранжировать по критичности.

### Задание со звёздочкой:
Переписать код так, как Вы считаете нужным, исправив все проблемы.

# Решение

### Дисклеймер
Так как в коде было много проблем, я переписал его полностью, вынеся всё, что не относится непосредственно к тестам, в условную директорию framework, где постарался приблизительно разделить зоны ответственности кода.
Цель - приблизительно обозначить подход, при котором в реальный тестовый проект желательно сразу закладывать масштабируемую архитектуру. 
Так как непонятно, как это предполагается запускать, я не обращал внимание на оптимизацию импортов, оставив вопросы организации запуска за скобками. 
В данном случае исхожу из предположения, что рабочей директорией при запуске pytest является собственно директория с проектом.  
Но хочу отметить, что в реальности вынес бы всю "обвязку" в другой репозиторий, если бы это был крупный проект, и там вопросы импортов решались бы по-другому - так, чтобы это корректно работало и локально, и в CI. 
Также в случае с крупным проектом файловая структура была бы намного сложнее. Для тестов приложения такого объёма, конечно, в усложнении нет нужды.

Честно говоря, я далеко не сразу понял, что же именно тестируется :) Сначала подумал, что API, где лежат картинки, 
и только когда начал формировать из этого нечто похожее на тестовый фреймворк, осознал, что само "приложение" 
находится в том же файле - собственно, мы тестируем пару функций `get_urls()` и `u()`. 
Но было уже поздно, поэтому их самих я тоже переписал и получилось, что они задействуют те же компоненты "фреймворка", что и тест :)

В списке ниже в обобщённом виде отразил проблемы, которые заметил, с отметками по исправлению, при этом не старался ограничить себя десятью пунктами. 
Однако, постарался приблизительно отранжировать их по степени критичности от большей к меньшей, поэтому можно рассматривать первые 10 пунктов как решение задачи.
P.S. К сожалению, проверить решение не удалось, так как Яндекс с этим токеном выдаёт "не авторизован".


### Проблемы в коде

1. Токен зашит прямо в коде. Для тестового окружения на внутреннем контуре это допустимо, но для публичного - нет: такие вещи должны храниться в защищённом хранилище (vault) и попадать в код через переменные окружения. _Однако, поскольку мне неизвестны предполагаемые условия запуска этих тестов, для сохранения работоспособности я оставил токен в коде. Роль переменных окружения будет играть файл с константами._
2. Весь код в одном файле - и вспомогательные методы, и сами тесты. Лучше разнести отдельно. _Вынесено в отдельный "фреймворк"._
3. Тесты должны быть воспроизводимыми, поэтому наличие случайного выбора из набора пород в параметризации нежелательно. _Убрал случайность, оставил все три._
4. Все урлы и прочие используемые в разных местах значения разбросаны текстом по всему коду. Такое лучше выносить в константы в одном месте, чтобы было проще менять и сложнее - допустить опечатку. _Вынесено в отдельный файл констант._
5. Присутствуют повторяющиеся действия, которые можно было бы оптимизировать. _Повторения убраны._
6. Не используются фикстуры - в них лучше вынести действия, связанные с подготовкой теста (и возвращением исходного состояния системы, если это требуется).
5. Пустой `__init__` в классе YaUploader. Можно использовать для чего-то полезного, например, для токена, или убрать. _Задействован для создания полезных атрибутов._
6. Совершенно нет документации. _Добавлено некоторое минимальное количество докстрингов и аннотаций типов, но не к "приложению"._
7. У проверок нет понятного описания на случай, если они не пройдены. _Описания добавлены._
6. У однотипных методов разный порядок позиционных аргументов с одинаковым значением. _Унифицировано._
2. Оба метода в классе YaUploader не используют обращение к экземпляру, поэтому могли бы быть статическими. Или можно вынести задействовать общие атрибуты экземпляра. _Сделано обращение к атрибутам экземпляра, содержащим общие для всех методов значения._
3. В конце обоих методов в классе YaUploader неиспользуемые имена переменных. _Убраны._
4. Нет никакой интеграции с системами генерации отчётов. Поскольку я не знаю, имеется ли в нашем гипотетическом проекте их поддержка, не стал добавлять, но в реальности для простоты использовал бы allure. В отчёты в этом случае ложились бы шаги, совершаемые в тестах, и все запросы/ответы сервисов.
5. Много мелких несоответствий PEP8. _Исправлены, но вообще такие вещи должны форматтером правиться. Поэтому проблема - его отсутствие._
6. В словаре params (это query parameters запроса) в методе upload_photos_to_yd булевое значение ключа `overwrite` написано строкой. Этого не нужно делать - requests сам умеет преобразовывать питонячьи словари в корректный формат перед отправкой запроса. _Исправлено._
7. В методе create_folder параметр добавлен в урл с помощью строкового форматирования. Этого не нужно делать - для query parameters у всех методой requests есть отдельный параметр. _Исправлено._
8. Многочисленные проблемы с неймингом: однобуквенное название функции; разные названия одинаковых по смыслу сущностей; смысл имени не соответствует значению и т.д. _По возможности исправлено._
9. Не ошибка, но может осложнить отладку: в некоторых местах исопльзуются цепочки вызовов вроде `return res.json().get('message', [])`. Если что-то не сработает в середине такой цепочки (например, метод json() работает только при наличии JSON в теле ответа), то будет не очень информативная ошибка. _Переделывать не стал, так как это скорее перестраховка._
10. Нет никакого ожидания в случае, когда что-то загружается на Яндекс.диск. Может возникнуть надобность добавить _неявное_ ожидание - например, с проверкой, что уже появилось нужное количество записей.
11. Зачем-то `assert True` посередине теста :) _Убрано._
12. Также с целью воспроизводимости лучше не делать ветвлений внутри теста, а делать отдельные тесты для каждого случая. _Оставил как есть, потому что точно не знаю, при каком из вариантов какой ответ должен прийти._
13. Написан тест только на часть функциональности, то есть тестами покрыто далеко не всё. Хотя задание состоит только в том, чтобы провалидировать имеющийся код, всё же считаю нужным подсветить эту проблему.
14. Вопрос предпочтений: делать тестовые функции внутри классов или нет (pytest позволяет оба подхода). На мой взгляд, в классы объединять удобнее для разделения по сьютам, если проект большой. Но можно и через файлы разбивать, кому как нравится. Поэтому оставил, как есть.
