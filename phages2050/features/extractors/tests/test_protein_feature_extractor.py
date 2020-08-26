from phages2050.features.extractors.proteins import ProteinFeatureExtractor


def test_normalize_static_method_with_source_as_str():
    """
    This test check if _normalize method remove blank chars
    from the beginning and end of the protein sequence as well
    as check if the returned sequence is in uppercase
    """

    protein_sequence = " makinellrestttnsnsigrpnlvaltrattkliysdivatqrtnqpvaa "
    normalized_sequence = ProteinFeatureExtractor._normalize(protein_sequence)

    expected_sequence = "MAKINELLRESTTTNSNSIGRPNLVALTRATTKLIYSDIVATQRTNQPVAA"

    assert normalized_sequence == expected_sequence
