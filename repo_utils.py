import os
import os.path
import hashlib
from flask import current_app
from werkzeug import secure_filename


class Repo(object):

    def __init__(self):
        pass

    @property
    def config_path(self):
        return current_app.config.get('REPO_PATH', 'repo')

    def get_file_path(self, name, prefix=""):
        folder = os.path.splitext(name)[0][:2]
        path = os.path.join(self.config_path, 'no-git-objects/%s'%prefix, folder)

        if not os.path.exists(path):
            os.makedirs(path)

        return os.path.join(path, name)

    def sha1(self, s):
        m = hashlib.sha1()
        m.update(s)
        return m.hexdigest()

    def add_item(self, data, name):
        name = secure_filename(name)
        path = self.get_file_path(name)

        if not os.path.exists(path):
            with open(path, 'wb') as w_file:
                w_file.write(data)
        return path

    def save(self, file_obj, name=None, is_sha1=False):
        name = secure_filename(name) if name else None
        data = file_obj.read()

        if name and is_sha1:
            self.add_item(data, name)
        else:
            sha1 = self.sha1(data)

            tmp_name = file_obj.filename if name is None else name
            ext = os.path.splitext(tmp_name)[-1]
            sha1_name = "%s%s" % (sha1, ext)
            path = self.add_item(data, sha1_name)

            if name and name != sha1_name:
                target = self.get_file_path(name, 'links')
                if os.path.exists(target):
                    os.remove(target)
                # use relative path to create symlink instead of absolute path
                path = os.path.relpath(path, os.path.dirname(target))
                os.symlink(path, target)

        return name if name else sha1_name

    def get_file(self, name):
        name = secure_filename(name)
        path = self.get_file_path(name)
        if not os.path.exists(path):
            path = self.get_file_path(name, 'links')
        return path


repo_obj = Repo()


def get_repo():
    return repo_obj
