# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import uuid, os, string, random
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator

class Account(models.Model):
	uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	sess = models.CharField(max_length=255)