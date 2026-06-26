"""JSON log formatter must stay valid JSON even with quotes/newlines in the message."""
import json
import logging

from app.core.logging import JsonFormatter


def test_json_formatter_escapes_special_characters():
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg='broke "this" \n and that',
        args=(),
        exc_info=None,
    )
    parsed = json.loads(formatter.format(record))
    assert parsed["msg"] == 'broke "this" \n and that'
    assert parsed["level"] == "INFO"
