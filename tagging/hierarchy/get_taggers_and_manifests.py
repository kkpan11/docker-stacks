# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from tagging.hierarchy.images_hierarchy import ALL_IMAGES
from tagging.manifests.manifest_interface import ManifestInterface
from tagging.taggers.tagger_interface import TaggerInterface


def get_taggers_and_manifests(
    short_image_name: str | None,
) -> tuple[list[TaggerInterface], list[ManifestInterface]]:
    if short_image_name is None:
        return [], []

    image_description = ALL_IMAGES[short_image_name]
    parent_taggers, parent_manifests = get_taggers_and_manifests(
        image_description.parent_image
    )
    return (
        parent_taggers + image_description.taggers,
        parent_manifests + image_description.manifests,
    )
