"""
To run tests with coverage, use the following commands:

coverage run --branch --source=app1,app2 ./manage.py test

To generate an HTML report, run the following code:

coverage html --omit=accounts/*migrations* -d coverage-report
"""

from django.test import TestCase, Client

from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django import forms

from accounts.models import User, UserProfile, create_user_profile
from accounts.forms import (UserCreateForm, UserUpdateForm,
                            UserProfileUpdateForm, must_be_empty)
from projects.models import Skill

user_test_data = {
    'username': 'test_user',
    'email': 'testing@gmail.com',
    'password': 'Testing17!'
}

user_test_data_incorrect = {
    'username': 'test_user',
    'email': 'testing2gmail.com',
    'password': 'Testing17!'
}


class TestDataMixin(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_user(**user_test_data)
        skill1 = Skill.objects.create(name='Python Developer')
        skill2 = Skill.objects.create(name='Designer')
        self.user1.userprofile.skills.add(skill1, skill2)

        self.client = Client()
        self.csrf_client = Client(enforce_csrf_checks=True)

    def tearDown(self):
        self.user1.delete()


################################
########## View Tests ##########
################################
class AccountsViewTests(TestDataMixin):
    def test_signup_view(self):
        response = self.client.get(reverse_lazy('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')
        self.assertTrue('Sign Up' in str(response.content))
        self.assertTrue('form' in response.context_data)
        self.assertIsInstance(response.context['form'], UserCreateForm)

    def test_signin_view(self):
        response = self.client.get(reverse_lazy('accounts:signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signin.html')
        self.assertTrue('Sign In' in str(response.content))
        self.assertIsInstance(response.context['form'], AuthenticationForm)
        self.assertTrue(self.client.login(email='testing@gmail.com', password='Testing17!'))

    def test_logout_view(self):
        response = self.client.get(reverse_lazy('accounts:signin'))
        self.assertTemplateUsed(response, 'accounts/signin.html')
        self.assertEqual(response.status_code, 200)

        self.client.login(email='testing@gmail.com', password='Testing17!')

        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)

    def test_userprofile_view(self):
        response = self.client.get(reverse('accounts:signin'))
        self.assertEqual(response.status_code, 200)

        self.client.login(email='testing@gmail.com', password='Testing17!')

        response = self.client.get(reverse('accounts:profile', kwargs={'username': 'test_user'}))
        self.assertEqual(response.status_code, 200)

    def test_userprofile_update_view(self):
        response = self.client.get(reverse('accounts:signin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signin.html')

        self.client.login(email='testing@gmail.com', password='Testing17!')

        response = self.client.get(reverse('accounts:update_profile', kwargs={'username': 'test_user'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_edit.html')
        self.assertIsInstance(response.context['form'], UserUpdateForm)
        self.assertIsInstance(response.context['form2'], UserProfileUpdateForm)

        response = self.client.post(
            reverse('accounts:update_profile', kwargs={'username': 'test_user'}),
            {
                'firstname': 'Test',
                'lastname': 'User'
            }
        )
        self.assertEqual(response.status_code, 200)


#################################
########## Model Tests ##########
#################################
class UserModelTests(TestDataMixin):
    def test_user_creation_no_email(self):
        with self.assertRaises(ValueError) as context:
            user = User.objects.create_user(
                username='test_user',
                email='',
                password='Testing17!',
            )
        self.assertTrue('Users must have an email address.' in context.exception)

    def test_user_creation_no_username(self):
        user = User.objects.create_user(
            username='',
            email='testing123@gmail.com',
            password='test123!'
        )
        username = user.username
        self.assertEqual(username, 'testing123')

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email='superuser7@gmail.com',
            username='',
            password='Testing17!'
        )
        self.assertEqual(superuser.is_staff, True)
        self.assertEqual(superuser.is_superuser, True)

    def test_str(self):
        self.assertEqual(str(self.user1), '@test_user')

    def test_get_short_name(self):
        self.assertEqual(self.user1.get_short_name(), self.user1.username)

    def test_get_long_name(self):
        self.assertEqual(self.user1.get_long_name(), '@test_user (testing@gmail.com)')


class UserProfileModelTests(TestDataMixin):
    def test_userprofile_creation(self):
        userprofile = self.user1.userprofile
        userprofile.firstname = 'Test'
        userprofile.lastname = 'User'
        userprofile.save()
        skills = [skill for skill in userprofile.skills.all()]
        self.assertEqual(userprofile.firstname, 'Test')
        self.assertEqual(userprofile.lastname, 'User')
        self.assertEqual(str(userprofile), 'Test User')
        self.assertEqual('Python Developer', skills[0].name)
        self.assertEqual('Designer', skills[1].name)

    def test_get_absolute_url(self):
        pass


################################
########## Form Tests ##########
################################
class UserCreateFormTests(TestDataMixin):
    # def test_UserCreateForm_valid(self):
    #     form = UserCreateForm(data={
    #         'username': 'testing12345',
    #         'email': 'this_is_a_test@gmail.com',
    #         'honeypot': '',
    #         'password1': 'Testing17!',
    #         'password2': 'Testing17!'
    #     })
    #     self.assertTrue(form.is_valid())

    def test_create_invalid(self):
        form = UserCreateForm(data=user_test_data_incorrect)
        self.assertFalse(form.is_valid())

    def test_must_be_empty(self):
        value = 'not empty'
        with self.assertRaises(forms.ValidationError) as context:
            must_be_empty(value)
        self.assertTrue('Is not empty' in context.exception)


class UserUpdateFormTests(TestDataMixin):
    def test_update_valid(self):
        form = UserUpdateForm(data={
            'username': 'testing345',
            'email': 'testing_again123@gmail.com'
        })
        self.assertTrue(form.is_valid())


class UserProfileUpdateFormTests(TestDataMixin):
    def test_update_valid(self):
        form = UserProfileUpdateForm(data={
            'firstname': 'Test',
            'lastname': 'User',
            'bio': 'This is a test of the UserProfileUpdateForm!'
        })
        self.assertTrue(form.is_valid())

