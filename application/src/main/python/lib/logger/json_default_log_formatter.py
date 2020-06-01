"""
logging.Formatter subclass for logging default records in JSON format.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from .json_base_log_formatter import JSONBaseLogFormatter


class JSONDefaultLogFormatter(JSONBaseLogFormatter):
    """Log default record in JSON format."""

    log_fields = [
        'time',
        'level',
        'request_uuid',
        'msg',
        # 'request_time',
        # 'protocol',
        'method',
        # 'scheme',
        # 'host',
        # 'script_name',
        'path',
        # 'query_string',
        # 'full_path',
        # 'url',
        # 'server_port',
        # 'request_content_type',
        # 'request_size',
        # 'content_language',
        # 'remote_addr',
        # 'user_agent',
        # 'status_code',
        # 'response_content_type',
        # 'response_size',
        # 'duration',
        'stack_trace',
    ]
