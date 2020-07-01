# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

"""
API interface.
"""

import os
import shutil

from .constants import JUPYTERLAB
from .converters import convert_catalog_to_json
from .utils import (
    check_locale,
    compile_translations,
    create_new_language_pack,
    update_translations,
    extract_translations,
)


def check_locales(locales):
    """
    Check if a given list  of locale values is valid.

    Raises an exception if an invalid locale value is found.

    Parameters
    ----------
    locales: list
        List of locales
    """
    for locale in locales:
        if not check_locale(locale):
            raise Exception("Invalid locale '{locale}'".format(locale=locale))


def normalize_project(project):
    """
    FIXME:

    Parameters
    ----------
    project: str
        FIXME:
    """
    return project.lower().replace("-", "_")


def extract_package(package_repo_dir, project):
    """
    FIXME:
    """


def update_package(package_repo_dir, project, locales):
    """
    FIXME:
    """
    if locales:
        check_locales(locales)

    project = normalize_project(project)
    output_dir = os.path.join(package_repo_dir, project)

    if not os.path.isdir(output_dir):
        raise Exception(
            "Output dir `{output_dir}` not found!".format(output_dir=output_dir)
        )

    update_translations(package_repo_dir, output_dir, project, locales)


def compile_package(package_repo_dir, project, locales):
    """
    FIXME
    """
    if locales:
        check_locales(locales)

    project = normalize_project(project)
    output_dir = os.path.join(package_repo_dir, project)
    po_paths = compile_translations(output_dir, project, locales)
    for __, po_path in po_paths.items():
        output_path = os.path.dirname(po_path)
        convert_catalog_to_json(po_path, output_path, project)


def extract_language_pack(package_repo_dir, language_packs_repo_dir, project):
    """
    FIXME:
    """
    project = normalize_project(project)

    if project == JUPYTERLAB:
        output_dir = os.path.join(language_packs_repo_dir, project)
    else:
        output_dir = os.path.join(
            language_packs_repo_dir, "jupyterlab_extensions", project
        )
        os.makedirs(output_dir, exist_ok=True)

    extract_translations(package_repo_dir, output_dir, project)


def update_language_pack(package_repo_dir, language_packs_repo_dir, project, locales):
    """
    FIXME
    """
    if locales:
        check_locales(locales)

    project = normalize_project(project)

    if project == JUPYTERLAB:
        output_dir = os.path.join(language_packs_repo_dir, project)
    else:
        output_dir = os.path.join(
            language_packs_repo_dir, "jupyterlab_extensions", project
        )
        os.makedirs(output_dir, exist_ok=True)

    update_translations(package_repo_dir, output_dir, project, locales)


def compile_language_pack(language_packs_repo_dir, project, locales):
    """
    FIXME:
    """
    if locales:
        check_locales(locales)

    project = normalize_project(project)

    if project == JUPYTERLAB:
        output_dir = os.path.join(language_packs_repo_dir, project)
    else:
        output_dir = os.path.join(
            language_packs_repo_dir, "jupyterlab_extensions", project
        )

    po_paths = compile_translations(output_dir, project, locales)
    for locale, po_path in po_paths.items():
        output_path = os.path.dirname(po_path)
        json_path = convert_catalog_to_json(po_path, output_path, project)
        mo_path = po_path.replace(".po", ".mo")

        # Move to language pack folder
        language_packs_dir = os.path.join(language_packs_repo_dir, "language-packs")
        pkg_name = "jupyterlab-language-pack-{locale}".format(locale=locale)
        locale_language_pack_dir = os.path.join(
            language_packs_dir, pkg_name, pkg_name.replace("-", "_")
        )

        # Check if it exists, otherwise create it
        if not os.path.isdir(locale_language_pack_dir):
            create_new_language_pack(language_packs_dir, locale)

        if project == JUPYTERLAB:
            output_dir = os.path.join(locale_language_pack_dir)
        else:
            output_dir = os.path.join(locale_language_pack_dir, "extensions")

        shutil.move(mo_path, os.path.join(output_dir, os.path.basename(mo_path)))
        shutil.move(json_path, os.path.join(output_dir, os.path.basename(json_path)))