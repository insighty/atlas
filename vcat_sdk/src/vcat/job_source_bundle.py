"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.change_directory import ChangeDirectory


class JobSourceBundle(object):

    def __init__(self, bundle_name, target_path):
        self._bundle_name = bundle_name
        self._path = target_path

    def bundle(self):
        import tarfile

        with tarfile.open(self.job_archive(), "w:gz") as tar:
            tar.add(".")
            for item in tar:
                self._log().debug('Added %s to source bundle', item.name)
                if item.name == './main.py':
                    raise Exception('Cannot add main.py to job bundle - please rename!')

    def unbundle(self, path_to_save):
        import tarfile
        from distutils.dir_util import mkpath

        with tarfile.open(self.job_archive(), "r:gz") as tar:
            mkpath(path_to_save)
            with ChangeDirectory(path_to_save):
                tar.extractall()

    def cleanup(self):
        from os import remove
        from os.path import exists
        
        if exists(self.job_archive()):
            remove(self.job_archive())

    def job_archive_name(self):
        return self._bundle_name + ".tgz"

    def job_archive(self):
        return self._path + self.job_archive_name()

    def file_listing(self):
        import tarfile

        with tarfile.open(self.job_archive(), "r:gz") as tar:
            for tarinfo in tar:
                yield tarinfo.name

    def _log(self):
        from vcat.global_state import log_manager
        return log_manager.get_logger(__name__)
