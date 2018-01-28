"""
Field validators.
"""

__author__ = 'Phil Ratcliffe'

import re

from django.core.exceptions import ValidationError


def validate_service(value):
    """Raises a validation error if service is an invalid form."""
    # TODO: Update validation to meet requirements.
    if re.search('^[A-Za-z]+\d*$', value) is None:
        msg = "Must start with a letter and be followed by letter or digits."
        raise ValidationError(msg)


def validate_version(value):
    """Raises a validation error if version is not comprised of alpha
    characters only.
    """
    # TODO: Update validation to meet requirements.
    if re.search('(\d+)\.(\d+)\.(\d+)', value) is None:
        msg = "Invalid version number. Should be in the form:\
            number.number.number"

        raise ValidationError(msg)
