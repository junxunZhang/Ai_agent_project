from src.feature_sets import get_feature_sets


def test_feature_sets_include_expected_keys():
    feature_sets = get_feature_sets()
    assert 'absorbance_only' in feature_sets
    assert 'absorbance_plus_context' in feature_sets
    assert 'absorbance_255nm' in feature_sets['absorbance_only']
