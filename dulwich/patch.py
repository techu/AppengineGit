import difflib
import subprocess

def write_commit_patch(f, commit, contents, progress, version=None):
    try:
        p = subprocess.Popen(["diffstat"], stdout=subprocess.PIPE, 
                             stdin=subprocess.PIPE)
    except OSError, e:
        pass # diffstat not available?
    else:
        (diffstat, _) = p.communicate(contents)
        f.write(diffstat)
        f.write("\n")
    f.write(contents)


def write_blob_diff(f, (old_path, old_mode, old_blob), 
                       (new_path, new_mode, new_blob)):
    """Write diff file header.

    :param f: File-like object to write to
    :param (old_path, old_mode, old_blob): Previous file (None if nonexisting)
    :param (new_path, new_mode, new_blob): New file (None if nonexisting)
    """
    def blob_id(blob):
        if blob is None:
            return "0" * 7
        else:
            return blob.id[:7]
    def lines(blob):
        if blob is not None:
            return blob.data.splitlines(True)
        else:
            return []
    if old_path is None:
        old_path = "/dev/null"
    else:
        old_path = "a/%s" % old_path
    if new_path is None:
        new_path = "/dev/null"
    else:
        new_path = "b/%s" % new_path
    f.write("diff --git %s %s\n" % (old_path, new_path))
    if old_mode != new_mode:
        if new_mode is not None:
            if old_mode is not None:
                f.write("old file mode %o\n" % old_mode)
            f.write("new file mode %o\n" % new_mode) 
        else:
            f.write("deleted file mode %o\n" % old_mode)
    f.write("index %s..%s %o\n" % (
        blob_id(old_blob), blob_id(new_blob), new_mode))
    old_contents = lines(old_blob)
    new_contents = lines(new_blob)
    f.writelines(difflib.unified_diff(old_contents, new_contents, 
        old_path, new_path))