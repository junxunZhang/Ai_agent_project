from src.feature_sets import get_feature_sets


def test_feature_sets_include_expected_keys():
    feature_sets = get_feature_sets()
    assert 'all_absorbance_only' in feature_sets
    assert 'all_absorbance_plus_machine' in feature_sets
    assert 'all_absorbance_plus_machine_plus_personal' in feature_sets
    assert 'absorbance_255nm' in feature_sets['all_absorbance_only']
    assert 'absorbance_285nm' in feature_sets['all_absorbance_only']
    assert 'absorbance_295nm' in feature_sets['all_absorbance_only']
