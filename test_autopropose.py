import autopropose


def test_parse_conf_file():
    conf_file_contents = """
period=60
contract='none'
"""

    parsed = autopropose.parse_conf(conf_file_contents)
    assert parsed['period'] == '60'
    assert parsed['contract'] == 'none'
