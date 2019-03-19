import warnings

# right now pyscss raises FutureWarning in Python 3.7
# this silences the warning until it is fixed in the library
with warnings.catch_warnings():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    from scss.compiler import Compiler


def compile_scss(root_src_path, src_path, root_dst_path, dst_path):
    """Compile SCSS into CSS."""
    compiler = Compiler(root=root_src_path)

    # get content
    relative_src_path = src_path.relative_to(root_src_path)
    content = compiler.compile(relative_src_path)

    # write file
    new_dst_path = dst_path.with_suffix('.css')
    new_dst_path.write_text(content)

