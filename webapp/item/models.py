from django.db import models
from autoslug import AutoSlugField
from django_fsm import FSMField, transition
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(unique=True, populate_from="title")

    def __str__(self):
        return self.title


class Product(models.Model):
    """
    Product creation and handling works through states:
    draft / new / rejected / banned / accepted

    To help switch between states we will use
    Transitions and Conditions methods
    """

    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    slug = AutoSlugField(unique=True, populate_from="title")
    state = FSMField(default="draft")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Conditions
    def can_reject(self):
        # Only allow rejection if the product is in the 'new' state and the user is the owner
        return self.state == "new" and self.user == self.owner

    def can_ban(self):
        # Only allow banning if the product is in the 'new' state
        return self.state == "new"

    def can_accept(self):
        # Only allow acceptance if the product is in the 'new' state
        return self.state == "new"

    def can_move_to_new_from_rejected(self):
        # Only allow moving to 'new' state from 'rejected' if the product is in the 'rejected' state and the user is the owner
        return self.state == "rejected" and self.user == self.owner

    def is_admin(self):
        return self.owner.is_staff

    def is_owner(self, user):
        return self.owner == user

    # Transitions
    @transition(field=state, source="draft", target="new")
    def move_to_new(self):
        pass

    @transition(field=state, source="new", target="rejected")
    def reject(self):
        pass

    @transition(field=state, source="new", target="banned")
    def ban(self):
        pass

    @transition(field=state, source="new", target="accepted")
    def accept(self):
        pass

    @transition(field=state, source="rejected", target="new")
    def move_to_new_from_rejected(self):
        pass

    def __str__(self):
        return self.title
