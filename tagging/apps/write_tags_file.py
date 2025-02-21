#!/usr/bin/env python3
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import logging
from pathlib import Path

from tagging.apps.common_cli_arguments import common_arguments_parser
from tagging.hierarchy.get_taggers_and_manifests import (
    get_taggers_and_manifests,
)
from tagging.utils.docker_runner import DockerRunner
from tagging.utils.get_prefix import get_file_prefix, get_tag_prefix

LOGGER = logging.getLogger(__name__)


def write_tags_file(
    *,
    registry: str,
    owner: str,
    short_image_name: str,
    variant: str,
    tags_dir: Path,
) -> None:
    """
    Writes tags file for the image <registry>/<owner>/<short_image_name>:latest
    """
    LOGGER.info(f"Tagging image: {registry}/{owner}/{short_image_name}")
    taggers, _ = get_taggers_and_manifests(short_image_name)

    image = f"{registry}/{owner}/{short_image_name}:latest"
    file_prefix = get_file_prefix(variant)
    filename = f"{file_prefix}-{short_image_name}.txt"

    tags_prefix = get_tag_prefix(variant)
    tags = [f"{registry}/{owner}/{short_image_name}:{tags_prefix}-latest"]
    with DockerRunner(image) as container:
        for tagger in taggers:
            tagger_name = tagger.__class__.__name__
            tag_value = tagger.tag_value(container)
            LOGGER.info(
                f"Calculated tag, tagger_name: {tagger_name} tag_value: {tag_value}"
            )
            tags.append(
                f"{registry}/{owner}/{short_image_name}:{tags_prefix}-{tag_value}"
            )
    tags_dir.mkdir(parents=True, exist_ok=True)
    file = tags_dir / filename
    file.write_text("\n".join(tags))
    LOGGER.info(f"Tags file written to: {file}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    arg_parser = common_arguments_parser(
        registry=True, owner=True, short_image_name=True, variant=True, tags_dir=True
    )
    args = arg_parser.parse_args()

    write_tags_file(**vars(args))
