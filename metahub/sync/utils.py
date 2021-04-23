import os
from io import BytesIO
from urllib.error import HTTPError
from urllib.request import urlopen

from django.core.files.images import ImageFile
from wagtail.core.blocks import StreamValue
from wagtail.core.models import Collection

from metahub.core.models import metahubImage

def add_stream_child(stream_value: StreamValue, type_name: str, value):
    if stream_value.is_lazy:
        stream_value.stream_data.append({
            'type': type_name,
            'value': value
        })
    else:
        # let's not make it too easy
        python_value = stream_value.stream_block.child_blocks[type_name].to_python(value)
        stream_value.stream_data.append((type_name, python_value))


def add_fabrique_image(file_name, title=None, is_url=False,
                      overwrite=False, collection_name=None, **kwargs):
    """ Programmatically add a Fabrique wagtail image to the database.

    :param file_import_path: (External) path to import the image file
        data from.
    :param title: (optional) Title of the image
    :param collection: (optional) name of collection to add image to
    :return:
    """

    file_import_path = 'src/metahub/sync/bc_images/{}'.format(file_name)
    file_import_path = 'sync/{}'.format(file_name)  #MKR: changed this outside of repository

    title = title or file_name

    try:
        wagtail_image = metahubImage.objects.get(title=title)
        created = False
    except metahubImage.DoesNotExist:
        wagtail_image = metahubImage()
        wagtail_image.title = title
        created = True

    if not created and not overwrite:
        return wagtail_image

    for key, value in kwargs.items():
        setattr(wagtail_image, key, value)

    if is_url:
        try:
            with urlopen(file_import_path) as response:
                file_data = response.read()
        except HTTPError:
            return None
    else:
        with open(file_import_path, 'rb') as opened_file:
            file_data = opened_file.read()
    if not file_data:
        return None

    file = BytesIO(file_data)
    image = ImageFile(file, file_name)

    # collection = 'Beecollect Object Images'
    # if collection_name:
    #     try:
    #         collection = Collection.objects.get(
    #             name=collection_name
    #         )
    #     except Collection.DoesNotExist:
    #         collection = Collection.get_first_root_node().add_child(
    #             name=collection_name)
    #     except Collection.MultipleObjectsReturned:
    #         collection = Collection.objects.filter(
    #             name=collection_name
    #         ).first()
    #
    # wagtail_image.collection = collection
    wagtail_image.file = image
    wagtail_image.save()

    return wagtail_image
