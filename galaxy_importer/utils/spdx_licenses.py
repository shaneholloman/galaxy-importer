import json
import logging
from importlib.resources import files


log = logging.getLogger(__name__)

_SPDX_LICENSES = None
_SPDX_LICENSES_FILE = "spdx_licenses.json"


def _load_spdx():
    parent_module = __name__.rsplit(".", 1)[0]
    try:
        with (files(parent_module) / _SPDX_LICENSES_FILE).open("rb") as stream:
            return json.load(stream)
    except OSError as exc:
        log.warning(
            "Unable to open %s to load the list of acceptable open source licenses: %s",
            _SPDX_LICENSES_FILE,
            exc,
        )
        log.exception(exc)
        return {}


def _get_spdx():
    """Gets the spdx_license info, so it is only loaded from disk once."""
    global _SPDX_LICENSES

    if not _SPDX_LICENSES:
        _SPDX_LICENSES = _load_spdx()

    return _SPDX_LICENSES


def is_valid_license_id(license_id):
    """Check if license_id is valid and non-deprecated SPDX ID."""
    if license_id is None:
        return False

    valid_license_ids = _get_spdx()
    valid = valid_license_ids.get(license_id, None)
    if valid is None:
        return False

    # license was in list, but is deprecated
    if valid and valid.get("deprecated", None):  # noqa: SIM103
        return False

    return True
