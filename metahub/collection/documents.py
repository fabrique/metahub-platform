from django.conf import settings
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from starling.utils import render, if2context

from .models import BaseCollectionObject
from ..starling_metahub.molecules.interfaces import MoleculeObjectCardRegular


