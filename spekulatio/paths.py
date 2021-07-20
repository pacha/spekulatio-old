from pathlib import Path

spekulatio_code_path = Path(__file__).absolute().parent.parent
spekulatio_templates_path = spekulatio_code_path / "data" / "template-dirs"
default_input_dir_path = spekulatio_templates_path / "spekulatio-default"
