import yaml
import pytest

from spekulatio.commands.config.validate.validate_config import validate_config
from spekulatio.exceptions import SpekulatioConfigError


def test_empty_config():
    config_content = yaml.safe_load(
        r"""
    """
    )
    with pytest.raises(SpekulatioConfigError):
        validate_config(config_content)


def test_minimal_config():
    config_content = yaml.safe_load(
        r"""
        output_dir: build/
        input_dirs:
          - path: content/
    """
    )
    validate_config(config_content)


def test_empty_input_dirs_config():
    config_content = yaml.safe_load(
        r"""
        output_dir: build/
        input_dirs:
    """
    )
    with pytest.raises(SpekulatioConfigError):
        validate_config(config_content)


def test_extra_field_config():
    config_content = yaml.safe_load(
        r"""
        output_dir: build/
        input_dirs:
          - path: content/
        foo: bar
    """
    )
    with pytest.raises(SpekulatioConfigError):
        validate_config(config_content)


def test_presets_config():
    config_content = yaml.safe_load(
        r"""
        output_dir: build/
        input_dirs:
          - path: content/
            preset: site_content
    """
    )
    validate_config(config_content)


def test_wrong_preset_config():
    config_content = yaml.safe_load(
        r"""
        output_dir: build/
        input_dirs:
          - path: content/
            preset: foo
    """
    )
    with pytest.raises(SpekulatioConfigError):
        validate_config(config_content)


def test_actions_config():
    config_content = yaml.safe_load(
        r"""
        output_dir: build/
        input_dirs:
          - path: content/
            actions:
              - filetype: png
                action: copy
              - filetype: html
                action: html_to_html
              - filetype: json
                action: json_to_html
    """
    )
    validate_config(config_content)


def test_invalid_action_config():
    config_content = yaml.safe_load(
        r"""
        output_dir: build/
        input_dirs:
          - path: content/
            actions:
              - filetype: png
                action: this_doesnt_exist
    """
    )
    with pytest.raises(SpekulatioConfigError):
        validate_config(config_content)


def test_filetypes_config():
    config_content = yaml.safe_load(
        r"""
        filetypes:
          - name: html
            extensions: ['html', 'htm']
          - name: jpeg
            regex: '^.*\.(jpg|jpeg)'
        output_dir: build/
        input_dirs:
          - path: content/
            actions:
              - filetype: png
                action: copy
              - filetype: html
                action: html_to_html
              - filetype: json
                action: json_to_html
    """
    )
    validate_config(config_content)


def test_wrong_filetype_config():
    config_content = yaml.safe_load(
        r"""
        filetypes:
          - name:
            extensions: ['html', 'htm']
        output_dir: build/
        input_dirs:
          - path: content/
            preset: site_content
    """
    )
    with pytest.raises(SpekulatioConfigError):
        validate_config(config_content)


def test_empty_filetype_config():
    config_content = yaml.safe_load(
        r"""
        filetypes:
        output_dir: build/
        input_dirs:
          - path: content/
            preset: site_content
    """
    )
    with pytest.raises(SpekulatioConfigError):
        validate_config(config_content)


def test_filetype_scopes():
    config_content = yaml.safe_load(
        r"""
        filetypes:
          - name: html
            extensions: ['html', 'htm']
          - name: jpeg
            regex: '^.*\.(jpg|jpeg)'
            scope: 'filename'
          - name: has_foo
            regex: '^.*foo.*$'
            scope: 'full-path'
        output_dir: build/
        input_dirs:
          - path: content/
            preset: site_content
    """
    )
    validate_config(config_content)


def test_wrong_filetype_scopes():
    config_content = yaml.safe_load(
        r"""
        filetypes:
          - name: html
            extensions: ['html', 'htm']
            scope: 'full-path'
        output_dir: build/
        input_dirs:
          - path: content/
            preset: site_content
    """
    )
    with pytest.raises(SpekulatioConfigError):
        validate_config(config_content)

    config_content = yaml.safe_load(
        r"""
        filetypes:
          - name: has_foo
            regex: '^.*foo.*$'
            scope: 'foobar'
        output_dir: build/
        input_dirs:
          - path: content/
            preset: site_content
    """
    )
    with pytest.raises(SpekulatioConfigError):
        validate_config(config_content)
