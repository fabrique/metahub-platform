from typing import NamedTuple

from metahub.starling_metahub.molecules.interfaces import MoleculeLinkListRegular


class QuarkFooterBarColumn(NamedTuple):
    title: str = ''
    link_list: MoleculeLinkListRegular = MoleculeLinkListRegular()
