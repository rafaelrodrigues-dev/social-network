from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from publications.models import Publication

User = get_user_model()

class PublicationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Criar usuário para os testes
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_publication_creation(self):
        """Testa a criação básica de uma publicação"""
        publication = Publication.objects.create(
            text='Texto de teste',
            author=self.user
        )
        self.assertEqual(publication.text, 'Texto de teste')
        self.assertEqual(publication.author, self.user)
        self.assertIsNotNone(publication.created_at)

    def test_str_representation(self):
        """Testa a representação em string do modelo"""
        publication = Publication.objects.create(
            text='Texto teste',
            author=self.user
        )
        expected_str = f'{self.user.username} {publication.id}'
        self.assertEqual(str(publication), expected_str)

    def test_image_field_properties(self):
        """Testa as propriedades do campo de imagem"""
        img_field = Publication._meta.get_field('img')
        
        # Testa parâmetros do campo
        self.assertEqual(img_field.upload_to, 'publications/images/%Y/%m/%d/')
        self.assertTrue(img_field.blank)
        self.assertEqual(img_field.default, '')
        
        # Testa upload de imagem
        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake',
            content_type='image/jpeg'
        )
        publication = Publication.objects.create(
            text='Publicação com imagem',
            author=self.user,
            img=test_image
        )
        
        # Verifica formato do caminho
        upload_path = publication.img.name
        expected_path = publication.created_at.strftime('publications/images/%Y/%m/%d/')
        self.assertTrue(upload_path.startswith(expected_path))

    def test_auto_now_add_property(self):
        """Testa se created_at é definido automaticamente"""
        publication = Publication.objects.create(
            text='Teste de data',
            author=self.user
        )
        original_date = publication.created_at
        
        # Atualiza a publicação
        publication.text = 'Texto atualizado'
        publication.save()
        self.assertEqual(publication.created_at, original_date)

    def test_author_deletion_cascade(self):
        """Testa o comportamento de cascata ao deletar o autor"""
        publication = Publication.objects.create(
            text='Teste de deleção',
            author=self.user
        )
        user_id = self.user.id
        self.user.delete()
        
        # Verifica se a publicação foi deletada junto
        with self.assertRaises(Publication.DoesNotExist):
            Publication.objects.get(id=publication.id)
            
        # Verificação adicional
        self.assertFalse(Publication.objects.filter(author_id=user_id).exists())

    def test_field_verbose_names(self):
        """Testa os nomes amigáveis dos campos"""
        self.assertEqual(Publication._meta.get_field('text').verbose_name, 'Text')
        self.assertEqual(Publication._meta.get_field('img').verbose_name, 'Image')
        self.assertEqual(Publication._meta.get_field('author').verbose_name, 'author')

    def test_optional_image_field(self):
        """Testa o campo de imagem como opcional"""
        publication = Publication.objects.create(
            text='Publicação sem imagem',
            author=self.user
        )
        self.assertEqual(publication.img.name, '')