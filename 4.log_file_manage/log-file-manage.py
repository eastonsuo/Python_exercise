#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tarfile
import os
import ConfigParser


def log_file_manage(dir_path):
    name_list = []  # '15100,15101,15102'
    for root, dir, files in os.walk(dir_path):
        for file_name in files:
            if file_name.startswith('uwsgi_log.log.'):
                prefix = file_name.split('.')[2][:5]
                if prefix not in name_list:
                    name_list.append(prefix)

    name_list.sort()
    for name in name_list[:-1]:
        tar = tarfile.open(
            "{0}/uwsgi_log_{1}.tar.gz".format(dir_path, name), "a")
        for root, dir, files in os.walk(dir_path):
            for file_name in files:
                if file_name.startswith('uwsgi_log.log.' + name):
                    fullpath = os.path.join(root, file_name)
                    tar.add(fullpath)
        tar.close()

    for name in name_list[:-1]:
        for root, dir, files in os.walk(dir_path):
            for file_name in files:
                if file_name.startswith('uwsgi_log.log.' + name):
                    fullpath = os.path.join(root, file_name)
                    os.remove(fullpath)


def trigger_log_file_manage():
    cf = ConfigParser.ConfigParser()
    cf.read('uwsgi_config.ini')
    file_path = cf.get("uwsgi", "logto")

    def get_dir():
        dirs = file_path.split('/')
        return '/'.join(dirs[:-1]) + '/'
    dir_path = get_dir()
    log_file_manage(dir_path)


if __name__ == '__main__':
    # trigger_log_file_manage()
    log_file_manage('log-file-manage')
