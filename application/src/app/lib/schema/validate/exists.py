"""Schema Validation: Exists"""


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
                record_item = model.query.get(int(record_id))
                if record_item is None:
                    errors.setdefault(field, [])
                    errors[field].append(invalid_error)
                    break
                else:
                    record.append(record_item)

    return errors, record
