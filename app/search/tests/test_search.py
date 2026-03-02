from django.test import TestCase
from publications.models import Publication
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class TestSearchView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='johndoe', password='testpassword', first_name='John', last_name='Doe')
        self.publication = Publication.objects.create(text='A publication', author=self.user)
        self.publication2 = Publication.objects.create(text='bla bla', author=self.user)
        self.publication3 = Publication.objects.create(text='Another test', author=self.user2)

    def test_search_by_text_publication(self):
        """Test search by publication text"""
        search_term = 'A publication'
        response = self.client.get(
            reverse('search:search') + f'?q={search_term}',
            data={'q': search_term}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.publication, response.context['page_obj'])
        self.assertNotIn(self.publication2, response.context['page_obj'])
    
    def test_search_by_author_publication(self):
        """Test search by publication author"""
        search_term = 'testuser'
        response = self.client.get(
            reverse('search:search') + f'?q={search_term}',
            data={'q': search_term}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.publication, response.context['page_obj'])
        self.assertIn(self.publication2, response.context['page_obj'])

    def test_search_empty_query(self):
        """Test search with empty query"""
        response = self.client.get(reverse('search:search') + '?q=')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 0)
        self.assertEqual(response.context['query'], '')
        self.assertEqual(response.context['search_type'], 'posts')

    def test_search_no_results(self):
        """Test search with no results"""
        response = self.client.get(reverse('search:search') + '?q=nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 0)
        self.assertEqual(response.context['query'], 'nonexistent')

    def test_search_context_variables(self):
        """Test if all context variables are present"""
        response = self.client.get(reverse('search:search') + '?q=test')
        self.assertIn('page_obj', response.context)
        self.assertIn('query', response.context)
        self.assertIn('additional_query', response.context)
        self.assertIn('search_type', response.context)
        self.assertEqual(response.context['search_type'], 'posts')
        self.assertEqual(response.context['additional_query'], '&q=test')

    def test_search_uses_correct_template(self):
        """Test if correct template is used"""
        response = self.client.get(reverse('search:search') + '?q=publication')
        self.assertTemplateUsed(response, 'search/pages/search_results.html')

    def test_search_pagination(self):
        """Test search pagination"""
        for i in range(10):
            Publication.objects.create(text=f'publication test {i}', author=self.user)
        
        response = self.client.get(reverse('search:search') + '?q=publication&page=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 7)  # Default 7 per page

    def test_search_pagination_second_page(self):
        """Test second page pagination"""
        for i in range(10):
            Publication.objects.create(text=f'publication test {i}', author=self.user)
        
        response = self.client.get(reverse('search:search') + '?q=publication&page=2')
        self.assertEqual(response.status_code, 200)
        # Second page should have at least one item
        self.assertGreater(len(response.context['page_obj']), 0)

    def test_search_invalid_page_number(self):
        """Test search with invalid page number"""
        response = self.client.get(reverse('search:search') + '?q=publication&page=nonexistent')
        self.assertEqual(response.status_code, 200)
        # Should return the first page
        self.assertEqual(response.context['page_obj'].number, 1)

    def test_search_query_with_whitespace(self):
        """Test search with whitespace"""
        response = self.client.get(reverse('search:search') + '?q=  publication  ')
        self.assertEqual(response.status_code, 200)
        # Query should be stripped of extra spaces
        self.assertEqual(response.context['query'], 'publication')


class TestSearchUserView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user2 = User.objects.create_user(username='johndoe', password='testpassword', first_name='John', last_name='Doe')
        self.user3 = User.objects.create_user(username='jane_smith', password='testpassword', first_name='Jane')

    def test_search_user_by_username(self):
        """Test user search by username"""
        response = self.client.get(reverse('search:search_user') + '?q=testuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user, response.context['page_obj'])

    def test_search_user_by_first_name(self):
        """Test user search by first name"""
        response = self.client.get(reverse('search:search_user') + '?q=John')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user2, response.context['page_obj'])

    def test_search_user_by_last_name(self):
        """Test user search by last name"""
        response = self.client.get(reverse('search:search_user') + '?q=Doe')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user2, response.context['page_obj'])

    def test_search_user_empty_query(self):
        """Test user search with empty query"""
        response = self.client.get(reverse('search:search_user') + '?q=')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 0)
        self.assertEqual(response.context['query'], '')

    def test_search_user_no_results(self):
        """Test user search with no results"""
        response = self.client.get(reverse('search:search_user') + '?q=nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 0)

    def test_search_user_context_variables(self):
        """Test if all context variables are present in user search"""
        response = self.client.get(reverse('search:search_user') + '?q=test')
        self.assertIn('page_obj', response.context)
        self.assertIn('query', response.context)
        self.assertIn('additional_query', response.context)
        self.assertIn('search_type', response.context)
        self.assertEqual(response.context['search_type'], 'users')
        self.assertEqual(response.context['additional_query'], '&q=test')

    def test_search_user_uses_correct_template(self):
        """Test if correct template is used for user search"""
        response = self.client.get(reverse('search:search_user') + '?q=john')
        self.assertTemplateUsed(response, 'search/pages/search_user_results.html')

    def test_search_user_pagination(self):
        """Test user search pagination"""
        # create users with identical first_name so that a single query matches all of them
        for i in range(10):
            User.objects.create_user(username=f'user{i}', password='testpassword', first_name='common')
        
        response = self.client.get(reverse('search:search_user') + '?q=common&page=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 7)  # Default 7 per page

    def test_search_user_pagination_second_page(self):
        """Test second page user pagination"""
        for i in range(10):
            User.objects.create_user(username=f'user{i}', password='testpassword', first_name='common')
        
        response = self.client.get(reverse('search:search_user') + '?q=common&page=2')
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context['page_obj']), 0)

    def test_search_user_invalid_page_number(self):
        """Test user search with invalid page number"""
        response = self.client.get(reverse('search:search_user') + '?q=test&page=invalid')
        self.assertEqual(response.status_code, 200)
        # Should return the first page
        self.assertEqual(response.context['page_obj'].number, 1)

    def test_search_user_query_with_whitespace(self):
        """Test user search with whitespace"""
        response = self.client.get(reverse('search:search_user') + '?q=  john  ')
        self.assertEqual(response.status_code, 200)
        # Query should be stripped of extra spaces
        self.assertEqual(response.context['query'], 'john')
