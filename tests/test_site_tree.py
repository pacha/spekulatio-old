
from spekulatio.model import ActionMap
from spekulatio.model import Site


def test_site_from_directory(fixtures_path, tmp_path):

    content_path = fixtures_path / 'minimal_site' / 'content'
    site = Site(build_path=tmp_path, only_modified=False)
    site.from_directory(
        content_path,
        ActionMap([
            ('md', 'render'),
            ('any', 'copy'),
        ])
    )

    assert len(site.root.children) == 2
