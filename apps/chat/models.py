from django.db import models

class Conversation(models.Model):

    class ConversationTypeChoices(models.TextChoices):
        PRIVATE = "private", "Private"
        GROUP = "group", "Group"
