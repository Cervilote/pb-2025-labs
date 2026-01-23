#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ИСПРАВЛЕНИЕ ГЛУПОГО ИИ
Добавляем понимание простых фраз СРАЗУ
"""

import sqlite3
import json
from datetime import datetime
import requests
from urllib.parse import quote_plus
import re

class FixedAI:
    def __init__(self):
        print("⚡ Исправляю тупого ИИ...")
        self.setup_database()
        self.preload_knowledge()  # ЗАГРУЖАЕМ ЗНАНИЯ СРАЗУ!
    
    def setup_database(self):
        """Создаем/очищаем базу"""
        self.conn = sqlite3.connect('fixed_ai.db')
        self.cursor = self.conn.cursor()
        
        # Очищаем старые таблицы если есть
        self.cursor.execute("DROP TABLE IF EXISTS knowledge")
        self.cursor.execute("DROP TABLE IF EXISTS simple_responses")
        
        # Создаем новую умную таблицу
        self.cursor.execute('''
            CREATE TABLE simple_responses (
                id INTEGER PRIMARY KEY,
                trigger TEXT UNIQUE,
                response TEXT,
                category TEXT,
                learned_from_user BOOLEAN DEFAULT 0
            )
        ''')
        
        # Таблица для сложных знаний
        self.cursor.execute('''
            CREATE TABLE knowledge (
                id INTEGER PRIMARY KEY,
                question TEXT,
                answer TEXT,
                source TEXT,
                confidence INTEGER DEFAULT 1
            )
        ''')
        
        self.conn.commit()
        print("✓ Новая база создана")
    
    def preload_knowledge(self):
        """ЗАГРУЗКА БАЗОВЫХ ЗНАНИЙ ПРИ ЗАПУСКЕ"""
        basic_responses = [
            # Приветствия
            ("привет", "Привет! Наконец-то я научился понимать людей!", "greeting"),
            ("здравствуй", "Здравствуй! Как дела?", "greeting"),
            ("хай", "Хай! Что нового?", "greeting"),
            ("hello", "Hello! I'm working now!", "greeting"),
            
            # Системные
            ("тест", "✅ Тест пройден! Я живой!", "system"),
            ("работаешь", "Да! Исправленная версия работает!", "system"),
            ("ты тут", "Конечно! Готов к работе!", "system"),
            
            # Вопросы
            ("как дела", "Теперь отлично! Меня только что починили!", "question"),
            ("как ты", "Спасибо, исправно! А ты?", "question"),
            ("что делаешь", "Учусь понимать тебя лучше!", "question"),
            
            # Прощания
            ("пока", "Пока! Возвращайся!", "farewell"),
            ("до свидания", "До свидания! Был рад общению!", "farewell"),
            ("выход", "Завершаю работу. До встречи!", "farewell"),
            
            # Двоичный код (специально для вашего примера!)
            ("10100111", "🤖 О! Это двоичный код! В десятичной системе это 167", "number"),
            ("01010101", "Это 85 в десятичной системе!", "number"),
            ("11111111", "255 - максимальное 8-битное число!", "number"),
            
            # Простые вопросы
            ("кто ты", "Я твой ИИ, которого только что починили!", "identity"),
            ("что ты умеешь", "Отвечать на вопросы и учиться новому!", "capability"),
            ("ты умный", "Стараюсь! Помоги мне стать умнее!", "compliment"),
        ]
        
        for trigger, response, category in basic_responses:
            self.cursor.execute(
                "INSERT OR IGNORE INTO simple_responses (trigger, response, category) VALUES (?, ?, ?)",
                (trigger, response, category)
            )
        
        self.conn.commit()
        print(f"✓ Загружено {len(basic_responses)} базовых ответов")
        print("  В том числе понимаю двоичные числа!")
    
    def understand_query(self, query):
        """УМНЫЙ ПОИСК ОТВЕТА (сначала в базе, потом в интернете)"""
        query_lower = query.strip().lower()
        
        print(f"\n🔍 Анализ запроса: '{query}'")
        
        # 1. Сначала ищем ТОЧНОЕ совпадение
        self.cursor.execute(
            "SELECT response FROM simple_responses WHERE trigger = ?",
            (query_lower,)
        )
        exact = self.cursor.fetchone()
        if exact:
            print("  ✓ Найдено точное совпадение")
            return exact[0]
        
        # 2. Ищем вхождение триггера в запросе
        self.cursor.execute("SELECT trigger, response FROM simple_responses")
        all_triggers = self.cursor.fetchall()
        
        for trigger, response in all_triggers:
            if trigger in query_lower and len(trigger) > 2:
                print(f"  ✓ Найдено по ключу: '{trigger}'")
                return response
        
        # 3. Проверяем, является ли запрос двоичным числом
        if all(c in '01 ' for c in query_lower.replace(' ', '')):
            binary_str = query_lower.replace(' ', '')
            if 1 <= len(binary_str) <= 32:  # разумная длина
                try:
                    decimal = int(binary_str, 2)
                    response = f"🧮 {binary_str} в двоичной = {decimal} в десятичной"
                    # Сохраняем этот новый факт!
                    self.learn_new_fact(f"двоичное {binary_str}", response)
                    return response
                except:
                    pass
        
        # 4. Если не нашли - учимся
        return self.handle_unknown_query(query_lower)
    
    def search_internet(self, query):
        """Поиск ответа в интернете (работает в России)"""
        print(f"  🌐 Ищу в интернете: '{query}'...")
        
        # 1. Пробуем Яндекс (основной, работает в России)
        result = self.search_yandex(query)
        if result[0]:
            return result
        
        # 2. Пробуем DuckDuckGo (на случай если доступен)
        try:
            result = self.search_duckduckgo_api(query)
            if result[0]:
                return result
        except:
            pass
        
        return None, None
    
    def search_yandex(self, query):
        """Поиск через Яндекс (работает в России)"""
        try:
            # Используем мобильную версию Яндекс.Поиска
            url = f"https://yandex.ru/search/?text={quote_plus(query)}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
            }
            
            response = requests.get(url, headers=headers, timeout=8)
            if response.status_code == 200:
                html = response.text
                
                # Ищем краткий ответ (feature snippet)
                snippet_match = re.search(r'<div[^>]*class="[^"]*text-container[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
                if snippet_match:
                    snippet = re.sub(r'<[^>]+>', '', snippet_match.group(1)).strip()
                    if len(snippet) > 20:
                        print(f"  ✓ Найдено в Яндексе!")
                        return snippet[:500], "Яндекс"
                
                # Ищем первый результат поиска
                result_match = re.search(r'<li[^>]*class="[^"]*serp-item[^"]*"[^>]*>.*?<h2[^>]*>.*?<a[^>]*>(.*?)</a>', html, re.DOTALL | re.IGNORECASE)
                if result_match:
                    title = re.sub(r'<[^>]+>', '', result_match.group(1)).strip()
                    if title:
                        # Пытаемся найти описание
                        desc_match = re.search(r'<div[^>]*class="[^"]*text-container[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL | re.IGNORECASE)
                        description = ""
                        if desc_match:
                            description = re.sub(r'<[^>]+>', '', desc_match.group(1)).strip()[:200]
                        
                        answer = f"{title}"
                        if description:
                            answer += f"\n{description}"
                        
                        print(f"  ✓ Найдено в Яндексе!")
                        return answer[:500], "Яндекс"
                
                # Альтернативный паттерн для результатов
                alt_match = re.search(r'<h2[^>]*><a[^>]*href="[^"]*"[^>]*>(.*?)</a></h2>', html, re.DOTALL | re.IGNORECASE)
                if alt_match:
                    title = re.sub(r'<[^>]+>', '', alt_match.group(1)).strip()
                    if title and len(title) > 10:
                        print(f"  ✓ Найдено в Яндексе!")
                        return title[:500], "Яндекс"
                        
        except Exception as e:
            print(f"  ⚠ Ошибка поиска в Яндексе: {e}")
        
        return None, None
    
    def search_duckduckgo_api(self, query):
        """Поиск через DuckDuckGo API (резервный, если доступен)"""
        try:
            url = f"https://api.duckduckgo.com/?q={quote_plus(query)}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                if data.get('AbstractText'):
                    answer = data['AbstractText']
                    source = data.get('AbstractURL', 'DuckDuckGo')
                    print(f"  ✓ Найдено в DuckDuckGo!")
                    return answer, source
                
                if data.get('Answer'):
                    answer = data['Answer']
                    source = data.get('AbstractURL', 'DuckDuckGo')
                    print(f"  ✓ Найдено в DuckDuckGo!")
                    return answer, source
        except:
            pass
        
        return None, None
    
    def handle_unknown_query(self, query):
        """Обработка неизвестного запроса"""
        print(f"  ✗ Неизвестный запрос: '{query}'")
        
        # Пробуем найти в интернете
        internet_answer, source = self.search_internet(query)
        
        if internet_answer:
            # Сохраняем найденный ответ в базу знаний
            self.cursor.execute(
                "INSERT INTO knowledge (question, answer, source, confidence) VALUES (?, ?, ?, ?)",
                (query, internet_answer, source or "internet", 2)
            )
            # Также добавляем в простые ответы для будущего использования
            self.learn_new_fact(query, internet_answer)
            self.conn.commit()
            
            response = f"🌐 Найдено в интернете:\n{internet_answer}"
            if source and source != "DuckDuckGo":
                response += f"\n\nИсточник: {source}"
            return response
        
        # Если не нашли в интернете - предлагаем научить
        teach_response = f"Я не знаю, что ответить на '{query}'. Научи меня!"
        teach_response += "\nНапиши: научи [вопрос] -> [ответ]"
        
        # Сохраняем как неизвестный
        self.cursor.execute(
            "INSERT INTO knowledge (question, answer, source) VALUES (?, ?, ?)",
            (query, "UNKNOWN", "user")
        )
        self.conn.commit()
        
        return teach_response
    
    def learn_new_fact(self, question, answer):
        """Учим новому факту"""
        try:
            self.cursor.execute(
                "INSERT INTO simple_responses (trigger, response, category, learned_from_user) VALUES (?, ?, ?, ?)",
                (question.lower(), answer, "learned", 1)
            )
            self.conn.commit()
            print(f"  📚 Выучил: '{question}' -> '{answer}'")
        except:
            pass
    
    def process_teaching(self, command):
        """Обработка команды обучения"""
        # Формат: научи привет -> привет друг
        if '->' in command:
            parts = command.split('->', 1)
        elif '→' in command:  # другой вариант стрелки
            parts = command.split('→', 1)
        else:
            return "Используй формат: научи вопрос -> ответ"
        
        if len(parts) != 2:
            return "Неверный формат"
        
        question = parts[0].replace('научи', '').strip()
        answer = parts[1].strip()
        
        if not question or not answer:
            return "Нужен и вопрос и ответ"
        
        self.learn_new_fact(question, answer)
        return f"✅ Выучил! Теперь на '{question}' я отвечаю: '{answer}'"
    
    def show_stats(self):
        """Показываем статистику"""
        self.cursor.execute("SELECT COUNT(*) FROM simple_responses")
        total = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM simple_responses WHERE learned_from_user = 1")
        learned = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM knowledge WHERE answer = 'UNKNOWN'")
        unknown = self.cursor.fetchone()[0]
        
        success_rate = (total - unknown) / total * 100 if total > 0 else 0
        
        print(f"\n📊 СТАТИСТИКА ИСПРАВЛЕННОГО ИИ:")
        print(f"   Всего ответов в базе: {total}")
        print(f"   Выучено пользователем: {learned}")
        print(f"   Неизвестных запросов: {unknown}")
        print(f"   Успешность: {success_rate:.1f}%")
        print(f"   (а не 0% как раньше!)")
    
    def chat_loop(self):
        """Основной цикл чата"""
        print("\n" + "="*60)
        print("🤖 ИСПРАВЛЕННЫЙ ИИ ЗАПУЩЕН!")
        print("="*60)
        print("\nТеперь я понимаю:")
        print("• Приветствия (привет, здравствуй, хай)")
        print("• Двоичные числа (10100111, 01010101)")
        print("• Простые вопросы")
        print("• 🌐 Поиск в интернете (если не знаю ответ)")
        print("\nКоманды:")
        print("• 'статистика' - показать мои знания")
        print("• 'научи вопрос -> ответ' - научить меня")
        print("• 'выход' - завершить общение")
        print("="*60)
        
        while True:
            try:
                user_input = input("\n👤 Вы: ").strip()
                
                if not user_input:
                    continue
                
                # Проверяем специальные команды
                if user_input.lower() in ['выход', 'exit', 'quit']:
                    print("\n🤖 ИИ: Пока! Возвращайся!")
                    self.show_stats()
                    break
                
                elif user_input.lower() == 'статистика':
                    self.show_stats()
                    continue
                
                elif user_input.lower().startswith('научи'):
                    result = self.process_teaching(user_input)
                    print(f"🤖 ИИ: {result}")
                    continue
                
                # Обычный запрос
                response = self.understand_query(user_input)
                print(f"🤖 ИИ: {response}")
                
            except KeyboardInterrupt:
                print("\n\n🤖 ИИ: Прервано пользователем")
                break
            except Exception as e:
                print(f"🤖 ИИ: Ошибка: {e}")

# Запускаем
if __name__ == "__main__":
    ai = FixedAI()
    ai.chat_loop()