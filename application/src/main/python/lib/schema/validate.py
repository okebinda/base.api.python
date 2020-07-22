"""
Schema validation functions.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""


def unique(errors, model, field, value, *, update=None):
    """Validates that a record's field is unique.

    :param errors: The existing error map
    :type errors: dict
    :param model: The SQLAlchemy database model to check against
    :type model: flask_sqlalchemy.Model
    :param field: The model's property to check
    :type field: sqlalchemy.orm.attributes.InstrumentedAttribute
    :param value: The new value to check that must be unique
    :param update: An existing instance of the record to stop false positive
    :return: The updated errors map
    :rtype: dict
    """

    if value is not None and (update is None or
                              getattr(update, field.name) != value):
        query = model.query.filter(field == value).first()
        if query:
            errors.setdefault(field.name, [])
            errors[field.name].append("Value must be unique.")

    return errors


def unique_email(errors, model, field, value, *, update=None):
    """Validates that a record's email field is unique by comparing hashes.

    :param errors: The existing error map
    :type errors: dict
    :param model: The SQLAlchemy database model to check against
    :type model: flask_sqlalchemy.Model
    :param field: The model's property to check
    :type field: sqlalchemy.orm.attributes.InstrumentedAttribute
    :param value: The new value to check that must be unique
    :param update: An existing instance of the record to stop false positive
    :return: The updated errors map
    :rtype: dict
    """

    if (value is not None
            and isinstance(value, str)
            and (update is None or getattr(update, field.name) != value)):
        temp_user = model(email=value)
        query = model.query.filter(
            model.email_digest == temp_user.email_digest).first()
        if query:
            errors.setdefault(field.name, [])
            errors[field.name].append("Value must be unique.")

    return errors


def exists(errors, model, field, pkey, *, missing_error=None,
           invalid_error=None):
    """Validates that a record's related record (via ID) exists in the
    database.

    :param errors: The existing error map
    :type errors: dict
    :param model: The SQLAlchemy database model to check against
    :type model: flask_sqlalchemy.Model
    :param field: The property being checked
    :type field: str
    :param pkey: The ID of the record that should exist
    :type pkey: int
    :param missing_error: Error message if ID is missing
    :type missing_error: str
    :param invalid_error: Error message if ID is not valid
    :type invalid_error: str
    :return: The updated errors map; the existing record if found
    :rtype: (dict, Model)
    """
    # pylint: disable=no-else-break

    if missing_error is None:
        missing_error = "Missing data for required field."

    if invalid_error is None:
        invalid_error = "Invalid value."

    record = None

    # basic test for ID existing
    if not pkey:
        errors.setdefault(field, [])
        errors[field].append(missing_error)

    # ID exists, move on
    else:

        # ID is a single int
        if isinstance(pkey, int) or (isinstance(pkey, str)
                                     and pkey.isnumeric()):
            record = model.query.get(int(pkey))
            if record is None:
                errors.setdefault(field, [])
                errors[field].append(invalid_error)

        # List if IDs
        elif isinstance(pkey, list):
            record = []
            for record_id in pkey:
                if isinstance(record_id, int) or (isinstance(record_id, str)
                                                  and record_id.isnumeric()):
                    record_item = model.query.get(int(record_id))
                    if record_item is None:
                        errors.setdefault(field, [])
                        errors[field].append(invalid_error)
                        break
                    else:
                        record.append(record_item)

    return errors, record
