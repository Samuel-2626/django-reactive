
from django_unicorn.components import UnicornView
from books.models import Book


class BookView(UnicornView):
    title: str = ""
    books = Book.objects.none()

    def hydrate(self):
        self.books = Book.objects.all()

    def add_book(self):
        if self.title != "":
            book = Book(title=self.title)
            book.save()

        self.title = ""

    def delete_book(self, id):
        try:
            book = Book.objects.get(id=id)
            book.delete()
        except:
            pass
