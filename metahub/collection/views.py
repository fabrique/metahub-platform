from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect

from metahub.sync.management.commands.beecollect_import import BeecollectImporter


def synchronise(request):
    if request.user.is_authenticated:
        try:
            BeecollectImporter().start(
                beecollect_folder=settings.BEECOLLECT_DATA_FOLDER,
                sync_folder=settings.BEECOLLECT_SYNC_FOLDER,
            )
            messages.success(request, "Successfully synchronised data.")
        except Exception as e:
            messages.error(request, f"Something went wrong: {e}.")
    return redirect("collection_basecollectionobject_modeladmin_index")
