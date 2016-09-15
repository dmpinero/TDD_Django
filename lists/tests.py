from django.template.loader import render_to_string
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase

from lists.models import Item
from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    # La respuesta a la request / (método home_page) es la página home.html
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', request=request)
        #self.assertEqual(response.content.decode(), expected_html)

    # Guardar petición POST
    def test_home_page_can_save(self):
        request = HttpRequest()                        # Establecer petición
        request.method = 'POST'                        # Establecer método de la petición
        request.POST['item_text'] = 'A new list item'  # Almacenar dentro de la petición un elemento con un valor

        response = home_page(request)                  # Obtener plantilla a través de la vista (controlador)

        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': request.POST['item_text']},
            request=request
        )
        #self.assertEqual(response.content.decode(), expected_html)

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()  # Guardar item en la base de datos

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()  # Guardar item en la base de datos

        saved_items = Item.objects.all()  # Recuperar items de la base de datos
        self.assertEqual(saved_items.count(), 2)  # Número de elementos que se esperan recuperar: 2

        first_saved_item = saved_items[0]   # Acceder al primer elemento
        second_saved_item = saved_items[1]  # Acceer al segundo elemento
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')