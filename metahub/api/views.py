# from django.http import JsonResponse
#
#
# from .serializers import BaseCollectionObjectSerializer, StoryPageSerializer
#
#
# from ..collection.models import BaseCollectionObject
# from ..stories.models import MetaHubStoryPage
#
#
# def get_object_by_inventory_number(request):
#     if request.method == 'GET':
#         object_id = request.GET.get('id')
#
#         if object_id:
#             try:
#                 object = BaseCollectionObject.objects.get(bc_inventory_number=object_id)
#             except BaseCollectionObject.DoesNotExist:
#                 return JsonResponse({'error': 'Object with that inventory number does not exist',
#                                      'data': None})
#             else:
#                 serializer = BaseCollectionObjectSerializer(object)
#                 return JsonResponse({'error': None,
#                                   'data': serializer.data })
#         else:
#             return JsonResponse({'error': 'Please supply an inventory number through the id parameter',
#                           'data': None})
#     else:
#         return JsonResponse({'error': '405: Method Not Allowed',
#                              'data': None})
#
#
# def get_story_by_id(request):
#     if request.method == 'GET':
#         story_id = request.GET.get('id')
#
#         if story_id:
#             try:
#                 story = MetaHubStoryPage.objects.live().get(rest_api_id=story_id)
#             except MetaHubStoryPage.DoesNotExist:
#                 return JsonResponse({'error': 'Story with that id does not exist or it is not live.',
#                                      'data': None})
#             else:
#                 serializer = StoryPageSerializer(story)
#                 return JsonResponse({'error': None,
#                                      'data': serializer.data})
#         else:
#             return JsonResponse({'error': 'Please supply a story id through the id parameter. The id can be found in the api_id panel of the story page in the CMS.',
#                                  'data': None})
#     else:
#         return JsonResponse({'error': '405: Method Not Allowed',
#                              'data': None})
