import json
import time
import requests
from typing import Dict, List, Any
import sqlite3
from datetime import datetime
import subprocess
import importlib
import sys

class SelfEvolvingAI:
    def __init__(self, name="EvoAI"):
        self.name = name
        self.knowledge_db = "ai_knowledge.db"
        self.code_file = "ai_core.py"
        self.memory = {}
        self.session_history = []
        self.init_databases()
        
    def init_databases(self):
        """Инициализация баз данных"""
        conn = sqlite3.connect(self.knowledge_db)
        c = conn.cursor()
        
        # Таблица знаний
        c.execute('''CREATE TABLE IF NOT EXISTS knowledge
                    (id INTEGER PRIMARY KEY,
                     topic TEXT,
                     content TEXT,
                     source TEXT,
                     timestamp DATETIME)''')
        
        # Таблица кодовых улучшений
        c.execute('''CREATE TABLE IF NOT EXISTS code_improvements
                    (id INTEGER PRIMARY KEY,
                     problem TEXT,
                     old_code TEXT,
                     new_code TEXT,
                     improvement_type TEXT,
                     timestamp DATETIME,
                     success BOOLEAN)''')
        
        # Таблица запросов пользователя
        c.execute('''CREATE TABLE IF NOT EXISTS user_requests
                    (id INTEGER PRIMARY KEY,
                     request TEXT,
                     response TEXT,
                     learned_from BOOLEAN,
                     timestamp DATETIME)''')
        
        conn.commit()
        conn.close()
    
    def save_to_db(self, table_name: str, data: Dict):
        """Универсальный метод для сохранения данных в таблицу"""
        conn = sqlite3.connect(self.knowledge_db)
        c = conn.cursor()
        
        if table_name == 'user_requests':
            c.execute('''INSERT INTO user_requests (request, response, learned_from, timestamp)
                        VALUES (?, ?, ?, ?)''',
                     (data.get('request', ''), data.get('response', ''), 
                      data.get('learned_from', False), data.get('timestamp', datetime.now())))
        elif table_name == 'knowledge':
            c.execute('''INSERT INTO knowledge (topic, content, source, timestamp)
                        VALUES (?, ?, ?, ?)''',
                     (data.get('topic', ''), json.dumps(data.get('content', {})),
                      data.get('source', ''), data.get('timestamp', datetime.now())))
        elif table_name == 'code_improvements':
            c.execute('''INSERT INTO code_improvements 
                        (problem, old_code, new_code, improvement_type, timestamp, success)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                     (data.get('problem', ''), data.get('old_code', ''),
                      data.get('new_code', ''), data.get('improvement_type', ''),
                      data.get('timestamp', datetime.now()), data.get('success', False)))
        
        conn.commit()
        conn.close()
        
    def process_query(self, query: str) -> str:
        """Улучшенная обработка запроса с пониманием намерений"""
        # Глубокий анализ запроса
        analysis = self.analyze_query(query)
        
        print(f"📝 Анализ запроса: {len(analysis['keywords'])} ключевых слов найдено")
        if analysis['is_question']:
            print("❓ Обнаружен вопрос")
        
        learned_from = False
        response = None
        internet_info = None
        
        # ВСЕГДА ищем информацию в интернете (приоритет интернет-поиска)
        print("🔍 Ищу информацию в интернете...")
        
        # Пробуем все варианты поискового запроса
        for i, search_query in enumerate(analysis['search_variants'], 1):
            if i > 1:
                print(f"   Попытка {i}: '{search_query}'")
            internet_info = self.search_internet(search_query)
            if internet_info and internet_info.get('abstract') and len(internet_info.get('abstract', '')) > 30:
                print(f"✓ Найдена информация для варианта: '{search_query}'")
                break
        
        # Если не нашли, пробуем поиск по ключевым словам
        if not internet_info or not internet_info.get('abstract') or len(internet_info.get('abstract', '')) < 30:
            if analysis['keywords']:
                # Пробуем разные комбинации ключевых слов
                keyword_combinations = [
                    ' '.join(analysis['keywords'][:3]),
                    ' '.join(analysis['keywords'][:2]),
                    ' '.join(analysis['keywords'][:4]) if len(analysis['keywords']) >= 4 else None
                ]
                for keywords_query in keyword_combinations:
                    if keywords_query:
                        print(f"🔍 Пробую поиск по ключевым словам: {keywords_query}")
                        internet_info = self.search_internet(keywords_query)
                        if internet_info and internet_info.get('abstract') and len(internet_info.get('abstract', '')) > 30:
                            break
        
        # Если все еще не нашли, пробуем упрощенный поиск
        if not internet_info or not internet_info.get('abstract') or len(internet_info.get('abstract', '')) < 30:
            simplified = ' '.join(analysis['keywords'][:2]) if analysis['keywords'] else query[:50]
            if simplified and simplified != query:
                print(f"🔄 Пробую упрощенный поиск: {simplified}")
                internet_info = self.search_internet(simplified)
        
        # Проверяем, что информация действительно найдена и валидна
        if internet_info and internet_info.get('abstract') and len(internet_info.get('abstract', '').strip()) > 30:
            # Если нашли в интернете - используем это (приоритет интернет-поиска)
            response = self.generate_response(query, analysis, [internet_info])
            # Сохраняем новое знание
            self.save_knowledge(query, internet_info)
            learned_from = True
            print(f"✓ Источник: {internet_info.get('source', 'unknown')}")
        else:
            # Если в интернете не нашли, пробуем базу знаний
            knowledge = self.search_knowledge(query)
            if knowledge:
                response = self.generate_response(query, analysis, knowledge)
                print("ℹ Использую информацию из базы знаний")
            else:
                # Последняя попытка - пробуем еще раз с оригинальным запросом
                print("🔄 Последняя попытка поиска с оригинальным запросом...")
                internet_info = self.search_internet(query)
                
                if internet_info and internet_info.get('abstract') and len(internet_info.get('abstract', '').strip()) > 30:
                    response = self.generate_response(query, analysis, [internet_info])
                    self.save_knowledge(query, internet_info)
                    learned_from = True
                    print(f"✓ Найдена информация (последняя попытка)")
                else:
                    response = self.generate_fallback_response(query, analysis)
                    print("✗ Информация не найдена в интернете")
        
        # Сохраняем запрос и ответ
        self.save_to_db('user_requests', {
            'request': query,
            'response': response,
            'learned_from': learned_from,
            'timestamp': datetime.now()
        })
                
        # Анализируем, можно ли улучшить код на основе этого запроса
        self.analyze_for_improvement(query, response)
        
        return response
    
    def search_internet(self, query: str) -> Dict:
        """Мощный поиск с использованием множества источников"""
        import urllib.parse
        import re
        
        # Очищаем и оптимизируем запрос
        query = query.strip()
        if not query:
            return None
        
        # Нормализуем запрос для поиска
        query_encoded = urllib.parse.quote(query)
        query_lower = query.lower()
        
        # Пробуем несколько методов поиска
        results = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        # 1. Поиск через Яндекс - открываем первую найденную страницу
        try:
            from bs4 import BeautifulSoup
            yandex_url = f"https://yandex.ru/search/?text={query_encoded}&lr=213"  # lr=213 для России
            yandex_headers = headers.copy()
            yandex_headers['Referer'] = 'https://yandex.ru/'
            
            response = requests.get(yandex_url, timeout=10, headers=yandex_headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Ищем первую ссылку в результатах поиска
                first_link = None
                
                # Пробуем разные селекторы для поиска ссылок
                link_selectors = [
                    ('a', {'class': 'link'}),
                    ('a', {'class': 'serp-item__title-link'}),
                    ('a', {'class': 'OrganicTitle-Link'}),
                    ('h2', {'class': 'serp-item__title'}),
                    ('div', {'class': 'serp-item'}),
                ]
                
                for tag_name, attrs in link_selectors:
                    elements = soup.find_all(tag_name, attrs, limit=10)
                    for elem in elements:
                        # Ищем ссылку внутри элемента
                        link = None
                        if tag_name == 'a':
                            link = elem.get('href', '')
                        else:
                            link_elem = elem.find('a')
                            if link_elem:
                                link = link_elem.get('href', '')
                        
                        if link:
                            # Обрабатываем относительные ссылки Яндекс
                            if link.startswith('/search?'):
                                continue  # Пропускаем ссылки на поиск
                            
                            # Яндекс использует редиректы через /search/?lr=213&text=...
                            # Нужно найти прямую ссылку
                            if 'yandex.ru' in link or link.startswith('http'):
                                # Проверяем, что это не реклама
                                if not any(word in link.lower() for word in ['yabs', 'direct', 'adfox', 'реклама']):
                                    first_link = link
                                    break
                        
                        # Альтернативный способ - ищем data-атрибуты
                        if not first_link:
                            data_url = elem.get('data-url') or elem.get('href')
                            if data_url and data_url.startswith('http') and 'yandex.ru' not in data_url:
                                first_link = data_url
                                break
                    
                    if first_link:
                        break
                
                # Если не нашли через селекторы, пробуем найти все ссылки
                if not first_link:
                    all_links = soup.find_all('a', href=True, limit=20)
                    for link_elem in all_links:
                        href = link_elem.get('href', '')
                        # Пропускаем внутренние ссылки Яндекс и рекламу
                        if (href.startswith('http') and 
                            'yandex.ru' not in href and 
                            not any(word in href.lower() for word in ['yabs', 'direct', 'adfox', 'реклама', 'market.yandex'])):
                            first_link = href
                            break
                
                # Если нашли ссылку, открываем страницу и извлекаем контент
                if first_link:
                    try:
                        print(f"   Открываю страницу: {first_link[:80]}...")
                        page_response = requests.get(first_link, timeout=12, headers=yandex_headers, allow_redirects=True)
                        
                        if page_response.status_code == 200:
                            page_soup = BeautifulSoup(page_response.text, 'html.parser')
                            
                            # Удаляем ненужные элементы (скрипты, стили, навигация)
                            for tag in page_soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                                tag.decompose()
                            
                            # Ищем основной контент страницы
                            content_selectors = [
                                ('article', {}),
                                ('main', {}),
                                ('div', {'class': 'content'}),
                                ('div', {'class': 'post-content'}),
                                ('div', {'class': 'article-content'}),
                                ('div', {'id': 'content'}),
                                ('div', {'class': 'text'}),
                                ('div', {'class': 'entry-content'}),
                            ]
                            
                            page_text = None
                            for tag_name, attrs in content_selectors:
                                content_elem = page_soup.find(tag_name, attrs)
                                if content_elem:
                                    # Убираем ссылки и навигацию
                                    for unwanted in content_elem.find_all(['a', 'nav', 'ul', 'ol']):
                                        unwanted.decompose()
                                    
                                    text = content_elem.get_text(separator=' ', strip=True)
                                    if text and len(text) > 200:  # Минимальная длина контента
                                        page_text = text[:3000]  # Ограничиваем размер
                                        break
                            
                            # Если не нашли через селекторы, берем все параграфы
                            if not page_text:
                                paragraphs = page_soup.find_all('p', limit=10)
                                text_parts = []
                                for p in paragraphs:
                                    text = p.get_text(strip=True)
                                    if text and len(text) > 50:
                                        text_parts.append(text)
                                
                                if text_parts:
                                    page_text = ' '.join(text_parts)[:3000]
                            
                            # Если все еще нет текста, берем body
                            if not page_text:
                                body = page_soup.find('body')
                                if body:
                                    # Удаляем навигацию и меню
                                    for tag in body.find_all(['nav', 'header', 'footer', 'menu', 'aside']):
                                        tag.decompose()
                                    page_text = body.get_text(separator=' ', strip=True)[:3000]
                            
                            if page_text and len(page_text) > 100:
                                results.append({
                                    'source': 'yandex',
                                    'abstract': page_text,
                                    'url': first_link
                                })
                                print(f"   ✓ Извлечен контент со страницы ({len(page_text)} символов)")
                    except Exception as e:
                        # Если не удалось открыть страницу, возвращаемся к сниппетам
                        pass
                
                # Если не удалось открыть страницу, используем сниппеты из поиска
                if not results:
                    text_parts = []
                    yandex_selectors = [
                        ('li', {'class': 'serp-item'}),
                        ('div', {'class': 'serp-item'}),
                        ('div', {'class': 'Organic'}),
                    ]
                    
                    for tag_name, attrs in yandex_selectors:
                        elements = soup.find_all(tag_name, attrs, limit=3)
                        for elem in elements:
                            snippet = elem.find(['div', 'span'], class_=['text-container', 'snippet', 'text'])
                            if snippet:
                                text = snippet.get_text(strip=True)
                                if text and 40 < len(text) < 500:
                                    if not any(word in text.lower() for word in ['реклама', 'купить', 'цена']):
                                        text_parts.append(text)
                        
                        if text_parts:
                            break
                    
                    if text_parts:
                        combined_text = ' '.join(text_parts[:3])[:1800]
                        if len(combined_text) > 50:
                            results.append({
                                'source': 'yandex',
                                'abstract': combined_text,
                                'url': yandex_url
                            })
        except ImportError:
            pass  # BeautifulSoup не установлен
        except Exception as e:
            pass
        
        # 2. Попытка через DuckDuckGo Instant Answer API
        try:
            duckduckgo_url = f"https://api.duckduckgo.com/?q={query_encoded}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(duckduckgo_url, timeout=8, headers=headers)
            if response.status_code == 200:
                data = response.json()
                abstract_text = data.get('AbstractText', '')
                if abstract_text and len(abstract_text) > 20:
                    results.append({
                        'source': 'duckduckgo',
                        'abstract': abstract_text,
                        'url': data.get('AbstractURL', ''),
                        'related': [topic.get('Text', '') for topic in data.get('RelatedTopics', [])[:3] if topic.get('Text')]
                    })
        except Exception:
            pass
        
        # 3. Wikipedia API - пробуем разные варианты запроса
        wiki_queries = [
            query,  # Оригинальный запрос
            query.title(),  # С заглавной буквы
            query.capitalize(),  # Первая буква заглавная
        ]
        
        # Если запрос содержит несколько слов, пробуем каждое слово отдельно
        if ' ' in query:
            words = query.split()
            wiki_queries.append(' '.join([w.capitalize() for w in words]))
            wiki_queries.append('_'.join([w.capitalize() for w in words]))  # Для Wikipedia URL
        
        for wiki_query in wiki_queries[:3]:  # Ограничиваем количество попыток
            try:
                # Пробуем русскую версию
                wiki_url_ru = f"https://ru.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(wiki_query.replace(' ', '_'))}"
                response = requests.get(wiki_url_ru, timeout=8, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    extract = data.get('extract', '')
                    if extract and len(extract) > 20:
                        results.append({
                            'source': 'wikipedia',
                            'abstract': extract,
                            'title': data.get('title', ''),
                            'url': data.get('content_urls', {}).get('desktop', {}).get('page', '')
                        })
                        break  # Нашли, выходим
                
                # Пробуем английскую версию
                wiki_url_en = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(wiki_query.replace(' ', '_'))}"
                response_en = requests.get(wiki_url_en, timeout=8, headers=headers)
                if response_en.status_code == 200:
                    data = response_en.json()
                    extract = data.get('extract', '')
                    if extract and len(extract) > 20:
                        results.append({
                            'source': 'wikipedia_en',
                            'abstract': extract,
                            'title': data.get('title', ''),
                            'url': data.get('content_urls', {}).get('desktop', {}).get('page', '')
                        })
                        break
            except Exception:
                continue
        
        # 4. Если API не сработали, пробуем скрапинг Wikipedia
        if not results:
            try:
                from bs4 import BeautifulSoup
                # Пробуем разные варианты URL
                wiki_urls = [
                    f"https://ru.wikipedia.org/wiki/{urllib.parse.quote(query.replace(' ', '_'))}",
                    f"https://ru.wikipedia.org/wiki/{urllib.parse.quote(query.title().replace(' ', '_'))}",
                    f"https://en.wikipedia.org/wiki/{urllib.parse.quote(query.replace(' ', '_'))}",
                ]
                
                for wiki_url in wiki_urls:
                    try:
                        response = requests.get(wiki_url, timeout=8, headers=headers)
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.text, 'html.parser')
                            # Ищем основной контент
                            content_div = soup.find('div', {'id': 'mw-content-text'})
                            if not content_div:
                                content_div = soup.find('div', class_='mw-parser-output')
                            
                            if content_div:
                                # Убираем ненужные элементы
                                for tag in content_div.find_all(['sup', 'span', 'div', 'table', 'nav'], 
                                                               class_=['reference', 'mw-editsection', 'navbox', 'infobox']):
                                    tag.decompose()
                                
                                # Берем первые параграфы
                                paragraphs = content_div.find_all('p', limit=5)
                                text_parts = []
                                for p in paragraphs:
                                    text = p.get_text(strip=True)
                                    if text and len(text) > 30:  # Игнорируем очень короткие параграфы
                                        text_parts.append(text)
                                
                                if text_parts:
                                    combined_text = ' '.join(text_parts)[:2000]
                                    if len(combined_text) > 100:
                                        results.append({
                                            'source': 'wikipedia_scraped',
                                            'abstract': combined_text,
                                            'url': wiki_url
                                        })
                                        break
                    except Exception:
                        continue
            except ImportError:
                pass  # BeautifulSoup не установлен
            except Exception:
                pass
        
        # 5. Поиск через DuckDuckGo HTML (более надежный)
        if not results:
            try:
                from bs4 import BeautifulSoup
                search_url = f"https://html.duckduckgo.com/html/?q={query_encoded}"
                response = requests.get(search_url, timeout=10, headers=headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Пробуем разные селекторы для результатов
                    result_selectors = [
                        ('div', {'class': 'result'}),
                        ('div', {'class': 'web-result'}),
                        ('div', {'class': 'links_main'}),
                        ('a', {'class': 'result__snippet'}),
                    ]
                    
                    combined_text = []
                    for tag_name, attrs in result_selectors:
                        elements = soup.find_all(tag_name, attrs, limit=5)
                        for elem in elements:
                            text = elem.get_text(strip=True)
                            if text and len(text) > 30:
                                combined_text.append(text)
                        if combined_text:
                            break
                    
                    if combined_text:
                        results.append({
                            'source': 'web_search',
                            'abstract': ' '.join(combined_text[:3])[:1500],
                            'url': search_url
                        })
            except ImportError:
                pass
            except Exception:
                pass
        
        # 6. Резервный метод - поиск через Google
        if not results:
            try:
                from bs4 import BeautifulSoup
                google_url = f"https://www.google.com/search?q={query_encoded}&hl=ru"
                google_headers = headers.copy()
                google_headers['Referer'] = 'https://www.google.com/'
                
                response = requests.get(google_url, timeout=8, headers=google_headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Ищем описания результатов Google
                    google_selectors = [
                        ('div', {'class': 'VwiC3b'}),
                        ('span', {'class': 'st'}),
                        ('div', {'class': 's'}),
                        ('div', {'class': 'IsZvec'}),
                    ]
                    
                    text_parts = []
                    for tag_name, attrs in google_selectors:
                        elements = soup.find_all(tag_name, attrs, limit=5)
                        for elem in elements:
                            text = elem.get_text(strip=True)
                            if text and 40 < len(text) < 500:
                                text_parts.append(text)
                        if text_parts:
                            break
                    
                    if text_parts:
                        results.append({
                            'source': 'google',
                            'abstract': ' '.join(text_parts[:3])[:1500],
                            'url': google_url
                        })
            except ImportError:
                pass
            except Exception:
                pass
        
        # Возвращаем результат
        if results:
            # Берем первый успешный результат
            best_result = results[0]
            
            # Если есть несколько результатов, можем объединить
            if len(results) > 1 and len(best_result.get('abstract', '')) < 500:
                combined_abstract = ' '.join([r.get('abstract', '') for r in results[:2]])[:2000]
                return {
                    'source': 'multiple',
                    'abstract': combined_abstract,
                    'sources': [r.get('source', '') for r in results[:2]]
                }
            
            return best_result
        
        return None
    
    def save_knowledge(self, topic: str, content: Dict):
        """Сохранение новых знаний"""
        conn = sqlite3.connect(self.knowledge_db)
        c = conn.cursor()
        c.execute('''INSERT INTO knowledge (topic, content, source, timestamp)
                     VALUES (?, ?, ?, ?)''',
                 (topic, json.dumps(content), 'internet', datetime.now()))
        conn.commit()
        conn.close()
    
    def analyze_for_improvement(self, query: str, response: str):
        """Анализ возможности улучшения кода"""
        improvements = []
        
        # Проверяем типичные проблемы
        if "не знаю" in response.lower() or "не могу" in response.lower():
            improvements.append({
                'problem': 'Недостаток знаний',
                'solution': 'Расширить поисковые возможности'
            })
        
        if len(query.split()) > 20 and len(response.split()) < 10:
            improvements.append({
                'problem': 'Сложные запросы обрабатываются поверхностно',
                'solution': 'Улучшить анализ контекста'
            })
        
        # Если нашли возможные улучшения
        for imp in improvements:
            self.generate_code_improvement(imp)
    
    def generate_code_improvement(self, improvement: Dict):
        """Генерация улучшения кода"""
        try:
            # Читаем текущий код
            with open(self.code_file, 'r', encoding='utf-8') as f:
                current_code = f.read()
            
            # Генерируем улучшение (упрощенно)
            problem = improvement['problem']
            solution = improvement['solution']
            
            new_method = f'''
    def handle_{problem.lower().replace(" ", "_")}(self):
        """Автоматически сгенерированный метод для: {problem}"""
        # {solution}
        print("Реализация улучшения: {solution}")
        pass
'''
            
            # Добавляем новый метод в класс
            if "class SelfEvolvingAI" in current_code:
                updated_code = current_code.replace(
                    "class SelfEvolvingAI:",
                    f"class SelfEvolvingAI:\n{new_method}"
                )
                
                # Сохраняем улучшение в БД
                conn = sqlite3.connect(self.knowledge_db)
                c = conn.cursor()
                c.execute('''INSERT INTO code_improvements 
                           (problem, old_code, new_code, improvement_type, timestamp, success)
                           VALUES (?, ?, ?, ?, ?, ?)''',
                         (problem, "", new_method, 'auto_generated', datetime.now(), True))
                conn.commit()
                conn.close()
                
                # Обновляем файл (в реальной системе нужно быть осторожнее!)
                # with open(self.code_file, 'w', encoding='utf-8') as f:
                #     f.write(updated_code)
                
                print(f"[AI] Обнаружено улучшение: {problem}")
                
        except Exception as e:
            print(f"Ошибка генерации улучшения: {e}")
    
    def search_knowledge(self, query: str) -> List:
        """Поиск в существующих знаниях"""
        conn = sqlite3.connect(self.knowledge_db)
        c = conn.cursor()
        c.execute('''SELECT content FROM knowledge 
                     WHERE topic LIKE ? OR content LIKE ? 
                     ORDER BY timestamp DESC LIMIT 5''',
                 (f'%{query}%', f'%{query}%'))
        results = c.fetchall()
        conn.close()
        
        return [json.loads(r[0]) for r in results]
    
    def analyze_query(self, query: str) -> Dict:
        """Улучшенный анализ запроса с пониманием намерений"""
        query_lower = query.lower().strip()
        
        # Определяем тип запроса
        question_words = ['что', 'кто', 'где', 'когда', 'почему', 'как', 'какой', 'какая', 'какое', 
                         'сколько', 'зачем', 'откуда', 'куда', 'чем', 'чем']
        is_question = any(qw in query_lower for qw in question_words) or '?' in query
        
        # Извлекаем ключевые слова (убираем стоп-слова)
        stop_words = {'что', 'это', 'как', 'где', 'когда', 'почему', 'кто', 'какой', 'какая', 
                     'какое', 'сколько', 'зачем', 'откуда', 'куда', 'чем', 'и', 'в', 'на', 
                     'с', 'по', 'для', 'от', 'до', 'из', 'о', 'об', 'про', 'при', 'у', 'к',
                     'со', 'во', 'обо', 'под', 'над', 'перед', 'за', 'между', 'среди', 'а',
                     'но', 'или', 'ли', 'же', 'бы', 'был', 'была', 'было', 'были', 'есть',
                     'быть', 'стать', 'стал', 'стала', 'стало', 'стали', 'можно', 'нужно',
                     'надо', 'должен', 'должна', 'должно', 'должны', 'могу', 'можешь', 'может'}
        
        words = query_lower.split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        # Определяем тему запроса
        tech_terms = ['код', 'програм', 'алгоритм', 'функция', 'python', 'java', 'javascript',
                     'html', 'css', 'база данных', 'api', 'веб', 'сайт', 'приложение']
        is_tech = any(term in query_lower for term in tech_terms)
        
        science_terms = ['наука', 'физика', 'химия', 'биология', 'математика', 'теория']
        is_science = any(term in query_lower for term in science_terms)
        
        history_terms = ['история', 'война', 'революция', 'империя', 'царь', 'король']
        is_history = any(term in query_lower for term in history_terms)
        
        # Генерируем варианты поискового запроса
        search_variants = [query]
        
        # Если это вопрос, создаем варианты без вопросительных слов
        if is_question:
            for qw in question_words:
                if query_lower.startswith(qw):
                    variant = query[len(qw):].strip()
                    if variant:
                        search_variants.append(variant)
                    break
        
        # Добавляем вариант только с ключевыми словами
        if keywords:
            keywords_query = ' '.join(keywords[:5])  # Берем до 5 ключевых слов
            if keywords_query != query_lower:
                search_variants.append(keywords_query)
        
        return {
            'original': query,
            'length': len(query),
            'complexity': len(query.split()),
            'is_question': is_question,
            'keywords': keywords,
            'is_tech': is_tech,
            'is_science': is_science,
            'is_history': is_history,
            'search_variants': search_variants[:3]  # Берем до 3 вариантов
        }
    
    def generate_response(self, query: str, analysis: Dict, knowledge: List) -> str:
        """Улучшенная генерация ответа с учетом анализа запроса"""
        if knowledge:
            primary = knowledge[0]
            
            # Обрабатываем разные форматы данных
            abstract = None
            source = primary.get('source', 'unknown')
            
            if isinstance(primary, dict):
                abstract = primary.get('abstract', '')
                if not abstract:
                    abstract = primary.get('content', '')
            elif isinstance(primary, str):
                abstract = primary
            
            if abstract and len(abstract.strip()) > 0:
                # Форматируем ответ с указанием источника
                source_name = {
                    'yandex': 'Яндекс',
                    'duckduckgo': 'DuckDuckGo',
                    'wikipedia': 'Википедия',
                    'wikipedia_en': 'Wikipedia (English)',
                    'wikipedia_scraped': 'Википедия',
                    'web_search': 'Веб-поиск',
                    'google': 'Google',
                    'multiple': 'несколько источников',
                    'web': 'веб-сайт'
                }.get(source, source)
                
                # Умная обрезка текста - стараемся закончить на предложении
                text = abstract
                if len(text) > 2000:
                    # Ищем последнюю точку до 2000 символов
                    cut_point = text[:2000].rfind('.')
                    if cut_point > 1000:  # Если нашли точку достаточно далеко
                        text = text[:cut_point + 1]
                    else:
                        text = text[:2000] + "..."
                
                # Если это вопрос, начинаем ответ более естественно
                if analysis.get('is_question'):
                    response = f"📚 Вот что я нашел ({source_name}):\n\n{text}"
                else:
                    response = f"📚 Информация из {source_name}:\n\n{text}"
                
                # Добавляем URL если есть
                if 'url' in primary and primary['url']:
                    response += f"\n\n🔗 Подробнее: {primary['url']}"
                
                # Добавляем связанные темы если есть
                if 'related' in primary and primary['related']:
                    related = [r for r in primary['related'] if r and len(r.strip()) > 0]
                    if related:
                        response += f"\n\n📌 Связанные темы: {', '.join(related[:3])}"
                
                return response
        
        return "Я изучил ваш запрос, но не нашел достаточно информации. Попробуйте переформулировать вопрос."
    
    def generate_fallback_response(self, query: str, analysis: Dict) -> str:
        """Улучшенный ответ по умолчанию с предложениями"""
        suggestions = []
        
        if analysis.get('keywords'):
            keywords_str = ', '.join(analysis['keywords'][:3])
            suggestions.append(f"Попробуйте поискать: {keywords_str}")
        
        if analysis.get('is_question'):
            suggestions.append("Попробуйте переформулировать вопрос более конкретно")
        
        suggestion_text = "\n💡 " + "\n💡 ".join(suggestions) if suggestions else ""
        
        return f"К сожалению, я не смог найти точную информацию по вашему запросу.{suggestion_text}\n\nПопробую улучшить свои поисковые возможности для будущих запросов."
    
    def self_diagnose(self):
        """Самоанализ и предложение улучшений"""
        conn = sqlite3.connect(self.knowledge_db)
        c = conn.cursor()
        
        # Анализ успешности ответов
        c.execute('''SELECT COUNT(*) FROM user_requests 
                     WHERE learned_from = ?''', (True,))
        learned_count = c.fetchone()[0]
        
        c.execute('''SELECT COUNT(*) FROM user_requests''')
        total_count = c.fetchone()[0]
        
        success_rate = learned_count / total_count if total_count > 0 else 0
        
        print(f"\n=== САМОДИАГНОСТИКА ИИ ===")
        print(f"Всего запросов: {total_count}")
        print(f"Успешно изучено: {learned_count}")
        print(f"Процент успеха: {success_rate:.2%}")
        
        # Предложения по улучшению
        if success_rate < 0.3:
            print("\nПредлагаемые улучшения:")
            print("1. Расширить поисковые возможности")
            print("2. Добавить кэширование запросов")
            print("3. Улучшить анализ контекста")
        
        conn.close()

# Веб-интерфейс для взаимодействия
class AIWebInterface:
    def __init__(self, ai_core):
        self.ai = ai_core
    
    def run_web_server(self):
        """Запуск простого веб-сервера"""
        from flask import Flask, request, jsonify
        
        app = Flask(__name__)
        
        @app.route('/query', methods=['POST'])
        def handle_query():
            data = request.json
            query = data.get('query', '')
            
            if query:
                response = self.ai.process_query(query)
                return jsonify({
                    'response': response,
                    'timestamp': datetime.now().isoformat()
                })
            return jsonify({'error': 'No query provided'})
        
        @app.route('/stats', methods=['GET'])
        def get_stats():
            return jsonify({
                'name': self.ai.name,
                'knowledge_entries': self.get_knowledge_count(),
                'improvements_count': self.get_improvements_count()
            })
        
        print("Запуск веб-сервера на http://localhost:5000")
        app.run(debug=True, port=5000)
    
    def get_knowledge_count(self):
        conn = sqlite3.connect(self.ai.knowledge_db)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM knowledge')
        count = c.fetchone()[0]
        conn.close()
        return count
    
    def get_improvements_count(self):
        conn = sqlite3.connect(self.ai.knowledge_db)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM code_improvements')
        count = c.fetchone()[0]
        conn.close()
        return count

# Основная функция
def main():
    print("Инициализация самообучающегося ИИ...")
    
    # Создаем экземпляр ИИ
    ai = SelfEvolvingAI(name="EvoAI v0.1")
    
    # Запускаем в консольном или веб-режиме
    mode = input("Выберите режим (1 - консоль, 2 - веб): ")
    
    if mode == "1":
        # Консольный режим
        print("Введите запросы (или 'выход' для завершения)")
        while True:
            query = input("\nВаш запрос: ")
            if query.lower() in ['выход', 'exit', 'quit']:
                break
            
            response = ai.process_query(query)
            print(f"\nИИ: {response}")
            
            # Периодическая самодиагностика
            if len(ai.session_history) % 5 == 0:
                ai.self_diagnose()
    
    elif mode == "2":
        # Веб-режим
        interface = AIWebInterface(ai)
        interface.run_web_server()

if __name__ == "__main__":
    main()