import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("900x700")

        # Загрузка книг
        self.books = self.load_books()
        self.setup_ui()

    def setup_ui(self):
        # Поле ввода названия книги
        ttk.Label(self.root, text="Название книги:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.title_entry = ttk.Entry(self.root, width=40)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        # Поле ввода автора
        ttk.Label(self.root, text="Автор:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.author_entry = ttk.Entry(self.root, width=40)
        self.author_entry.grid(row=1, column=1, padx=10, pady=5)

        # Поле выбора жанра
        ttk.Label(self.root, text="Жанр:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.genre_var = tk.StringVar()
        genres = ["Роман", "Фантастика", "Детектив", "Биография", "Поэзия", "Другое"]
        self.genre_combo = ttk.Combobox(self.root, textvariable=self.genre_var, values=genres, state="readonly")
        self.genre_combo.grid(row=2, column=1, padx=10, pady=5)

        # Поле ввода количества страниц
        ttk.Label(self.root, text="Количество страниц:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.pages_entry = ttk.Entry(self.root)
        self.pages_entry.grid(row=3, column=1, padx=10, pady=5)

        # Кнопка добавления книги
        self.add_btn = ttk.Button(self.root, text="Добавить книгу", command=self.add_book)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтры
        ttk.Label(self.root, text="Фильтр по жанру:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.filter_genre_var = tk.StringVar(value="Все")
        self.filter_genre_combo = ttk.Combobox(
            self.root,
            textvariable=self.filter_genre_var,
            values=["Все"] + genres
        )
        self.filter_genre_combo.grid(row=5, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Фильтр по страницам (>):").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.filter_pages_entry = ttk.Entry(self.root)
        self.filter_pages_entry.grid(row=6, column=1, padx=10, pady=5)

        self.apply_filter_btn = ttk.Button(self.root, text="Применить фильтры", command=self.refresh_books_table)
        self.apply_filter_btn.grid(row=7, column=0, columnspan=2, pady=5)

        # Таблица книг
        ttk.Label(self.root, text="Список книг:").grid(row=8, column=0, columnspan=2, pady=10)
        columns = ("ID", "Название", "Автор", "Жанр", "Страниц")
        self.books_tree = ttk.Treeview(self.root, columns=columns, show="headings", height=15)

        for col in columns:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=120)

        self.books_tree.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")


        # Заполнение таблицы
        self.refresh_books_table()

    def load_books(self):
        if os.path.exists("books.json"):
            with open("books.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_books(self):
        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=2)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_var.get()
        pages_str = self.pages_entry.get().strip()

        # Валидация полей
        if not title:
            messagebox.showerror("Ошибка", "Название книги не может быть пустым")
            return
        if not author:
            messagebox.showerror("Ошибка", "Автор не может быть пустым")
            return
        if not genre:
            messagebox.showerror("Ошибка", "Выберите жанр")
            return

        # Валидация количества страниц
        try:
            pages = int(pages_str)
            if pages <= 0:
                messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
            return

        # Добавление книги
        book = {
            "id": len(self.books) + 1,
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages
        }
        self.books.append(book)
        self.save_books()
        self.refresh_books_table()

        # Очистка полей ввода
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_var.set("")
        self.pages_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", "Книга добавлена")

    def refresh_books_table(self):
        # Очистка таблицы
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)

        # Получение фильтров
        filter_genre = self.filter_genre_var.get()
        filter_pages_str = self.filter_pages_entry.get().strip()

        filtered_books = self.books

        # Фильтр по жанру
        if filter_genre != "Все":
            filtered_books = [b for b in filtered_books if b["genre"] == filter_genre]

        # Фильтр по количеству страниц
        if filter_pages_str:
            try:
                filter_pages = int(filter_pages_str)
                filtered_books = [b for b in filtered_books if b["pages"] > filter_pages]
            except ValueError:
                messagebox.showwarning("Предупреждение", "Некорректное значение для фильтра страниц")

                return

        # Заполнение таблицы отфильтрованными записями
        for book in filtered_books:
            self.books_tree.insert("", "end", values=(
                book["id"],
                book["title"],
                book["author"],
                book["genre"],
                book["pages"]
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
