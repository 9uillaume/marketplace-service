from django.core import mail
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Product, Category


class ProductViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="user1", password="password1", email="foo@bar.com"
        )
        self.staff_user = User.objects.create_user(
            username="staff_user", password="password", is_staff=True
        )
        self.category = Category.objects.create(title="Frames")
        self.product = Product.objects.create(
            title="Picasso", state="draft", category=self.category, owner=self.user
        )

    def test_move_to_new(self):
        url = reverse("product-move-to-new", kwargs={"pk": self.product.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.state, "new")

    def test_reject(self):
        url = reverse("product-reject", kwargs={"pk": self.product.pk})

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.product.state = "new"
        self.product.save()

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Log in as a staff user
        self.client.force_login(user=self.staff_user)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.state, "rejected")

        # Check email notification
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, f"Product State Change: {self.product.title}")
        self.assertEqual(email.to, [self.product.owner.email])
        self.assertIn("rejected", email.body)

    # def test_ban(self):
    # Similar to the reject test, follow a similar approach to test the ban endpoint

    # def test_accept(self):
    # Similar to the reject test, follow a similar approach to test the accept endpoint

    # def test_move_to_new_from_rejected(self):
    # Similar to the move_to_new test, follow a similar approach to test the move_to_new_from_rejected endpoint
