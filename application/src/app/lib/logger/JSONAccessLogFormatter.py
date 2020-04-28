"""logging.Formatter subclass for logging request/responses in JSON format."""

from .JSONBaseLogFormatter import JSONBaseLogFormatter


class JSONAccessLogFormatter(JSONBaseLogFormatter):
    """Log request/response in JSON format."""

    log_fields = [
        'time',
        # 'level',
        'request_uuid',
        # 'msg',
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
        # 'stack_trace',
    ]
