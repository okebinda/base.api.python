"""
logging.Formatter subclass for logging in JSON format.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""
# pylint: disable=consider-iterating-dictionary

from datetime import datetime, timezone
import json
import logging
import traceback

from flask import has_request_context, request, g


class JSONBaseLogFormatter(logging.Formatter):
    """Log event record in JSON format. Subclass this for finer control."""

    log_fields = [
        'time',
        'level',
        'request_uuid',
        'msg',
        'request_time',
        'protocol',
        'method',
        'scheme',
        'host',
        'script_name',
        'path',
        'query_string',
        'full_path',
        'url',
        'server_port',
        'request_content_type',
        'request_size',
        'content_language',
        'remote_addr',
        'user_agent',
        'status_code',
        'response_content_type',
        'response_size',
        'duration',
        'stack_trace',
    ]

    datetime_format = '%Y-%m-%dT%H:%M:%S.%f%z'

    def prep_record(self, record):
        """Prepare event record for logging.

        :param record: Record of event to be logged
        :type record: LogRecord
        :return: Transformed LogRecord object
        :trype: LogRecord
        """

        record.data = {
            'time': datetime.now(timezone.utc),
        }
        record.time = record.data['time'].strftime(self.datetime_format)
        record.level = record.levelname
        record.stack_trace = None
        if record.exc_info:
            record.stack_trace = ''.join(
                traceback.format_exception(*record.exc_info)
            ) if record.exc_info else ''
        return record

    def prep_request(self, record):
        """Prepare request for logging.

        :param record: Record of event to be logged
        :type record: LogRecord
        :return: Dictionary of request properties
        :trype: dict
        """
        # pylint: disable=unused-argument

        # available fields
        available_fields = [
            'request_uuid'
            'request_time',
            'protocol',
            'method',
            'scheme',
            'host',
            'script_name',
            'path',
            'query_string',
            'full_path',
            'url',
            'server_port',
            'request_content_type',
            'request_size',
            'content_language',
            'remote_addr',
            'user_agent',
        ]
        request_data = {key: None for key in available_fields}

        if has_request_context():

            if hasattr(g, 'request_uuid'):
                request_data['request_uuid'] = str(g.request_uuid)

            if hasattr(g, 'request_time'):
                request_data['request_time'] = g.request_time.strftime(
                    self.datetime_format)

            # request property : log name
            request_fields = {
                'method': 'method',
                'scheme': 'scheme',
                'host': 'host',
                'path': 'path',
                'full_path': 'full_path',
                'url': 'url',
                'content_type': 'request_content_type',
                'content_length': 'request_size',
                'content_language': 'content_language',
                'remote_addr': 'remote_addr',
            }
            request_data.update(
                [(request_fields[key], getattr(request, key))
                 for key in request_fields.keys() if hasattr(request, key)])

            if hasattr(request, 'environ'):

                # request.environ property : log name
                environ_fields = {
                    'REQUEST_URI': 'full_path',
                    'SERVER_PROTOCOL': 'protocol',
                    'HTTP_USER_AGENT': 'user_agent',
                    'HTTP_X_REAL_IP': 'remote_addr',
                    'SCRIPT_NAME': 'script_name',
                    'QUERY_STRING': 'query_string',
                    'SERVER_PORT': 'server_port',
                }
                request_data.update(
                    [(environ_fields[key], request.environ.get(key)) for
                     key in environ_fields.keys() if key in request.environ])

        return request_data

    def prep_response(self, record):
        """Prepare response for logging.

        :param record: Record of event to be logged
        :type record: LogRecord
        :return: Dictionary of response properties
        :trype: dict
        """
        # pylint: disable=no-self-use

        # available fields
        available_fields = [
            'status_code',
            'response_size',
            'duration',
        ]
        response_data = {key: None for key in available_fields}

        if hasattr(record, 'response'):

            # response property : log name
            response_fields = {
                'status_code': 'status_code',
                'content_type': 'response_content_type',
                'content_length': 'response_size',
            }
            response_data.update(
                [(response_fields[key], getattr(record.response, key))
                 for key in response_fields.keys()
                 if hasattr(record.response, key)])

        if (g.request_time and hasattr(record, 'data')
                and 'time' in record.data):
            time_delta = record.data['time'] - g.request_time
            response_data['duration'] = time_delta.total_seconds()

        return response_data

    def format(self, record):
        """Formats log record in JSON.

        :param record: Record of event to be logged
        :type record: LogRecord
        :return: JSON string of request/response fields
        :trype: str
        """

        log_data = {}

        # add record fields
        self.prep_record(record)
        log_data.update([(key, getattr(record, key)) for key
                         in self.log_fields if hasattr(record, key)
                         and getattr(record, key)])

        # add request fields
        request_data = self.prep_request(record)
        log_data.update([(key, request_data.get(key)) for key
                         in self.log_fields if request_data.get(key)])

        # add response fields
        response_data = self.prep_response(record)
        log_data.update([(key, response_data.get(key)) for key
                         in self.log_fields if response_data.get(key)])

        return json.dumps(log_data)
