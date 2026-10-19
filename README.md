# Summit

## Ідея сайту

Summit - сайт для пошуку гірських маршрутів та організованих сходжень. Юзер обирає країну та гору, переглядає фото, вид з вершини, маршрути, їхню складність і зупинки. Для маршруту можна знайти пропозиції організаторів із датами, ціною, контактами, умовами оренди спорядження та супроводу (цей етап поки під питанням).

Гора може мати кілька маршрутів, а маршрут - кілька пропозицій сходжень. Ціна, дати, оренда та супровід належать конкретній пропозиції. Маршрути додаються вручну з дозволених для використання джерел.

Зареєстрований юзер зможе редагувати профіль, зберігати сходження в обране та подавати заявки на участь. Адміністратор керуватиме каталогом і заявками. Сторінка «Про нас» міститиме опис проєкту й контакти.

Для початку передбачається декілька країн з невеликою к-стю пропозицій

## REST API

Базовий шлях: `/api/v1`. Дані передаються у JSON. Нижче - план API.

### Формати даних

ЦЕ ВСЕ ПРИКЛАДИ!!!

#### Country

```json
{
  "id": 1,
  "name": "Україна",
  "description": "Гори та подорожі Україною."
}
```

#### Mountain

```json
{
  "id": 1,
  "country_id": 1,
  "name": "Навчальна вершина",
  "height_m": 2800,
  "description": "Умовна гора.",
  "image_url": "https://example.com/mountain.jpg",
  "summit_view_url": "https://example.com/summit.jpg"
}
```

#### Route

```json
{
  "id": 1,
  "mountain_id": 1,
  "name": "Південний маршрут",
  "description": "Умовний маршрут.",
  "difficulty": "medium",
  "duration_days": 3,
  "source_url": null
}
```

#### Stop - зупинка маршруту

```json
{
  "id": 1,
  "route_id": 1,
  "position": 1,
  "name": "Перший табір",
  "altitude_m": 1800,
  "description": "Умовна зупинка для ночівлі."
}
```

#### Organizer

```json
{
  "id": 1,
  "name": "Приклад клубу",
  "description": "Навчальний організатор.",
  "email": "club@example.com",
  "phone": "+380000000000",
  "website_url": null
}
```

#### Trip - пропозиція сходження

```json
{
  "id": 1,
  "route_id": 1,
  "organizer_id": 1,
  "title": "Навчальне сходження",
  "start_date": "2027-06-10",
  "end_date": "2027-06-12",
  "price": "4500.00",
  "capacity": 8,
  "rental_available": true,
  "rental_details": "Спорядження за попередньою домовленістю; вартість уточнюється.",
  "guide_available": true,
  "support_details": "Супровід гіда включено.",
  "included_services": "Трансфер до початку маршруту.",
  "requirements": "Попередній досвід гірських походів.",
  "status": "open",
  "available_places": 8
}
```

#### User - профіль

```json
{
  "id": 1,
  "username": "climber",
  "email": "climber@example.com",
  "first_name": "Олена",
  "last_name": "Коваль"
}
```

#### Application - заявка

```json
{
  "id": 1,
  "user_id": 1,
  "trip_id": 1,
  "participants_count": 2,
  "comment": "Потрібно уточнити оренду.",
  "status": "pending",
  "created_at": "2027-01-10T12:00:00Z"
}
```

#### Favorite

```json
{
  "id": 1,
  "user_id": 1,
  "trip_id": 1,
  "created_at": "2027-01-10T12:00:00Z"
}
```

### Каталог

| Метод | Ендпоінт | Використання | Параметри / JSON-тіло | Відповідь |
| --- | --- | --- | --- | --- |
| GET | /countries | Список країн | — | 200, [Country] |
| GET | /countries/{id} | Переглянути країну | id | 200, Country |
| POST | /countries | Додати країну | поля Country | 201, Country |
| PATCH | /countries/{id} | Змінити країну | id; частина полів Country | 200, Country |
| DELETE | /countries/{id} | Видалити країну | id | 204 |
| GET | /mountains | Список гір | country_id, search, min_height, max_height; ordering: name, height_m | 200, [Mountain] |
| GET | /mountains/{id} | Переглянути гору | id | 200, Mountain |
| POST | /mountains | Додати гору | поля Mountain | 201, Mountain |
| PATCH | /mountains/{id} | Змінити гору | id; частина полів Mountain | 200, Mountain |
| DELETE | /mountains/{id} | Видалити гору | id | 204 |
| GET | /routes | Список маршрутів | mountain_id, search, difficulty; ordering: name, duration_days | 200, [Route] |
| GET | /routes/{id} | Переглянути маршрут | id | 200, Route |
| POST | /routes | Додати маршрут | поля Route | 201, Route |
| PATCH | /routes/{id} | Змінити маршрут | id; частина полів Route | 200, Route |
| DELETE | /routes/{id} | Видалити маршрут | id | 204 |
| GET | /organizers | Список організаторів | search | 200, [Organizer] |
| GET | /organizers/{id} | Переглянути організатора | id | 200, Organizer |
| POST | /organizers | Додати організатора | поля Organizer | 201, Organizer |
| PATCH | /organizers/{id} | Змінити організатора | id; частина полів Organizer | 200, Organizer |
| DELETE | /organizers/{id} | Видалити організатора | id | 204 |
| GET | /trips | Список сходжень | country_id, mountain_id, route_id, organizer_id, search (title), difficulty, min_price, max_price, start_date_from, rental_available, guide_available, status; ordering: price, start_date | 200, [Trip] |
| GET | /trips/{id} | Переглянути сходження | id | 200, Trip |
| POST | /trips | Додати сходження | поля Trip | 201, Trip |
| PATCH | /trips/{id} | Змінити сходження | id; частина полів Trip | 200, Trip |
| DELETE | /trips/{id} | Видалити сходження | id | 204 |

### Зупинки

| Метод | Ендпоінт | Використання | Параметри / JSON-тіло | Відповідь |
| --- | --- | --- | --- | --- |
| `GET` | `/routes/{route_id}/stops` | План зупинок за position | route_id | 200, [Stop] |
| `GET` | `/routes/{route_id}/stops/{id}` | Окрема зупинка | route_id, id | 200, Stop |
| `POST` | `/routes/{route_id}/stops` | Додати зупинку | route_id; поля Stop | 201, Stop |
| `PATCH` | `/routes/{route_id}/stops/{id}` | Редагувати зупинку | route_id, id; частина полів Stop | 200, Stop |
| `DELETE` | `/routes/{route_id}/stops/{id}` | Видалити зупинку | route_id, id | 204 |

### Реєстрація та профіль

| Метод | Ендпоінт | Використання | JSON-тіло | Відповідь |
| --- | --- | --- | --- | --- |
| `POST` | `/users` | Реєстрація | `{"username":"climber","email":"climber@example.com","password":"ExamplePass123!","first_name":"Олена","last_name":"Коваль"}` | 201, User; 409, зайняті username/email |
| `POST` | `/sessions` | Вхід | `{"username":"climber","password":"ExamplePass123!"}` | 201, `{"user": User}`; cookie сесії; 401, неправильні дані |
| `DELETE` | `/sessions/current` | Вихід | — | 204 |
| `GET` | `/users/me` | Свій профіль | — | 200, User |
| `PATCH` | `/users/me` | Змінити профіль | Будь-яка непорожня підмножина `{"email":"new@example.com","first_name":"Олена","last_name":"Коваль"}` | 200, User; 409, зайнятий email |

Реєстрація та вхід доступні всім. Сервер не повертає пароль.

### Заявки та обране

| Метод | Ендпоінт | Використання | Параметри / JSON-тіло | Відповідь |
| --- | --- | --- | --- | --- |
| `GET` | `/applications` | Список своїх заявок; для адміна — усіх | Необов'язкові status, trip_id | 200, [Application] |
| `GET` | `/applications/{id}` | Деталі своєї заявки; адмін — будь-якої | id | 200, Application |
| `POST` | `/applications` | Подати заявку | `{"trip_id":1,"participants_count":2,"comment":"Потрібна оренда."}` | 201, Application; 409, немає місць, сходження недоступне або заявка вже існує |
| `PATCH` | `/applications/{id}` | Змінити статус | id; `{"status":"cancelled"}` | 200, Application; 409, недопустима зміна або немає місць |
| `GET` | `/favorites` | Своє обране | — | 200, [Favorite] |
| `POST` | `/favorites` | Додати сходження в обране | `{"trip_id":1}` | 201, Favorite; 409, уже додано |
| `DELETE` | `/favorites/{id}` | Видалити власний запис обраного | id запису Favorite | 204 |

## Схема бази даних

<img width="736" height="604" alt="Знімок екрана 2026-10-19 032210" src="https://github.com/user-attachments/assets/f71cf53f-88ff-4a6a-b139-1a1f2ea97e51" />
