"""Tests for TESScut sector pointing lookup."""

from unittest import mock

import pytest
from astropy.coordinates import SkyCoord
from astropy.table import Table

from lksearch import TESSSearch


def _search_without_network():
    """Build a TESSSearch object without running any MAST queries."""
    search = TESSSearch.__new__(TESSSearch)
    search.SkyCoord = SkyCoord(109.49, 21.84, unit="deg")
    search.target_search_string = "TIC 125843782"
    return search


def test_sector_is_looked_up_by_number():
    """Pointings are found by sector number, not by row position."""
    search = _search_without_network()
    sectors = Table({"sector": [1, 1751]})
    with mock.patch("lksearch.TESSSearch.Tesscut.get_sectors", return_value=sectors):
        result = search._get_tesscut_info()
    assert list(result["sequence_number"]) == [1, 1751]


def test_unknown_sector_raises():
    """A sector with no pointing information raises a ValueError."""
    search = _search_without_network()
    sectors = Table({"sector": [1, 99999]})
    patch = mock.patch("lksearch.TESSSearch.Tesscut.get_sectors", return_value=sectors)
    with patch, pytest.raises(ValueError, match="sector 99999"):
        search._get_tesscut_info()
