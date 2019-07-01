from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList


class CustomJSONRenderer(JSONRenderer):
    """
    This is used as the default way to render JSON responses in django rest framework
    due to a requirement by the front end to return lists inside dictionaries with the following format:
    {'data': <list content>}
    """
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = {'data': data} if type(data) is ReturnList else data
        return super(CustomJSONRenderer, self).render(data, accepted_media_type, renderer_context)
