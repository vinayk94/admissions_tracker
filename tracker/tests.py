from django.test import TestCase, Client
from django.urls import reverse
from .models import AdmissionPost

class AdmissionPostModelTest(TestCase):
    def setUp(self):
        AdmissionPost.objects.create(
            degree_type='BS',
            major='Computer Science',
            university='Test University',
            country='Test Country',
            application_round='Fall 2024',
            status='APPLIED',
            gpa=3.8,
            test_type='GRE',
            test_score=320,
            student_type='DOMESTIC'
        )

    def test_admission_post_creation(self):
        post = AdmissionPost.objects.get(university='Test University')
        self.assertEqual(post.major, 'Computer Science')
        self.assertEqual(post.status, 'APPLIED')

class AdmissionPostViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.create_post_url = reverse('create_post')

    def test_home_view(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/home.html')

    def test_create_post_view(self):
        response = self.client.get(self.create_post_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/create_post.html')

    def test_create_post_form_submission(self):
        post_data = {
            'degree_type': 'MS',
            'major': 'Data Science',
            'university': 'Test University',
            'country': 'Test Country',
            'application_round': 'Fall 2024',
            'status': 'APPLIED',
            'gpa': 3.9,
            'test_type': 'GRE',
            'test_score': 325,
            'student_type': 'INTERNATIONAL'
        }
        response = self.client.post(self.create_post_url, data=post_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful form submission
        self.assertTrue(AdmissionPost.objects.filter(major='Data Science').exists())