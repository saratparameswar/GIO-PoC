from src.get_binders import get_data

TEMPLATE_CONFIG_PATH = "config/templates_config.yaml"

def test_aircraft_policy_broad_coverage():
    template_name = get_data(config_path=TEMPLATE_CONFIG_PATH, f_name="test_binder_files/Aircraft-policy-broad-coverage-1.docx")
    assert template_name == "Aircraft Policy - Broad Coverage"