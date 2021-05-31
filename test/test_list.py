import os


def test_zets_exist_path(zet_list_paths):
    assert all(os.path.exists(sample_zet) for sample_zet in zet_list_paths)
    assert all(os.path.isfile(sample_zet) for sample_zet in zet_list_paths)


def test_zets_name(zet_list):
    assert all("/" not in sample_zet for sample_zet in zet_list)
    assert all("\\" not in sample_zet for sample_zet in zet_list)
