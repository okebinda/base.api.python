"""Schema Validation: Unique"""


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
