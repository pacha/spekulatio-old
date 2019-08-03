
import sass

def compile_scss(root_src_path, src_path, root_dst_path, dst_path):
    """Compile SCSS into CSS."""

    # get content
    content = sass.compile(filename=str(src_path))

    # write file
    new_dst_path = dst_path.with_suffix('.css')
    new_dst_path.write_text(content)

