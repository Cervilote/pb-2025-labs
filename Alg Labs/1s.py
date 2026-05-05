
books = [
    {"title": "Приколы. Веселые рожицы с наклейками.", "author": "Самовар", "year": 2011, "pages": 8},
    {"title": "Славарь сатаны", "author": "Бирс Амброз", "year": 1906, "pages": 350},
    {"title": "Никто не дурак", "author": "Руссо Ричард", "year": 1993, "pages": 549},
    {"title": "Краткая история тракторов по-украински", "author": "Левацкая Марина", "year": 2005, "pages": 320},
    {"title": "Дающий", "author": "Лоури Лоис", "year": 2011, "pages": 256},
    {"title": "Дневник войны со свиньями", "author": "Касарес Адольфо бьой", "year": 2010, "pages": 320},
    {"title": "Вожделеющее семя", "author": "Бёрджес Энтони", "year": 2002, "pages": 288},
    {"title": "Траектория краба", "author": "Грасс Гюнтер", "year": 2004, "pages": 288},
    {"title": "Гвоздья гнева", "author": "Стейнбек Джон", "year": 2007, "pages": 592},
    {"title": "Электропрохладительный кислотный тест", "author": "Вульф Том", "year": 2006, "pages": 424},
    {"title": "Бегом с ножницами", "author": "Берроуз Огюстен", "year": 2007, "pages": 302},
    {"title": "Продюсер козьей морды", "author": "Донцова Дарья", "year": 2008, "pages": 384}
]

def show_books(books_list):
    print("\n" + "=" * 50)
    for i, book in enumerate(books_list, 1):
        print(f"{i}. {book['title']}")
        print(f"   Автор: {book['author']}")
        print(f"   Год: {book['year']}, Страниц: {book['pages']}")
    print("=" * 50 + "\n")

def sort_books(books_list, key_field):
    return sorted(books_list, key=lambda x: x[key_field])

while True:
    print("\n1-по названию, 2-по автору, 3-по году, 4-по страницам, 0-выход")
    choice = input("Выберите сортировку: ")
    if choice == "0":
        break
    elif choice in ["1", "2", "3", "4"]:
        keys = {"1": "title", "2": "author", "3": "year", "4": "pages"}
        books = sort_books(books, keys[choice])
        show_books(books)