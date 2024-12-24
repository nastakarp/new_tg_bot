import requests

class NewsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://newsapi.org/v2/top-headlines"

    def get_news(self, category=None, query=None, page=1) -> str:
        print(f"Запрос новостей: категория={category}, запрос={query}, страница={page}")

        params = {
            'apiKey': self.api_key,
            'language': 'en',
            'pageSize': 1,
            'page': page,
            'sortBy': 'relevancy',
        }
        if category:
            params['category'] = category
        if query:
            if len(query) < 3:
                return "Введите более конкретный запрос (не менее 3 символов)."
            params['q'] = query

        response = requests.get(self.url, params=params)

        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            if articles:
                news = ""
                for i, article in enumerate(articles, 1):
                    title = article['title']
                    description = article.get('description', 'Описание не доступно.')
                    url = article['url']
                    news += f"{i}. {title}\n{description}\nПодробнее: {url}\n\n"
                print("Новости получены успешно.")
                return news
            else:
                print("Новости не найдены.")
                return "К сожалению, ничего не найдено. Попробуйте уточнить запрос."
        else:
            print(f"Ошибка при получении новостей, статус: {response.status_code}")
            return "Ошибка при получении новостей. Попробуйте позже."