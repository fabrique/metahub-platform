# from datetime import timedelta, datetime
#
# from elasticsearch_dsl import Facet, Range
#
#
# class DateHistogramFacet(Facet):
#     """
#     Overrriden from dsl because it somehow does not support year as an interval.
#     Which is what we need... >:C
#     """
#     agg_type = 'date_histogram'
#
#     DATE_INTERVALS = {
#         'month': lambda d: (d+timedelta(days=32)).replace(day=1),
#         'week': lambda d: d+timedelta(days=7),
#         'day': lambda d: d+timedelta(days=1),
#         'hour': lambda d: d+timedelta(hours=1),
#         'year': lambda d: (d+timedelta(days=365)).replace(day=1),
#         # 'year': lambda d: d.replace(year=d.year+1),
#     }
#
#     def __init__(self, **kwargs):
#         kwargs.setdefault("min_doc_count", 0)
#         super(DateHistogramFacet, self).__init__(**kwargs)
#
#     def get_value(self, bucket):
#         if not isinstance(bucket['key'], datetime):
#             # Elasticsearch returns key=None instead of 0 for date 1970-01-01,
#             # so we need to set key to 0 to avoid TypeError exception
#             if bucket['key'] is None:
#                 bucket['key'] = 0
#             # Preserve milliseconds in the datetime
#             return datetime.utcfromtimestamp(int(bucket['key']) / 1000.0)
#         else:
#             return bucket['key']
#
#     def get_value_filter(self, filter_value):
#         return Range(**{
#             self._params['field']: {
#                 'gte': filter_value,
#                 'lt': self.DATE_INTERVALS[self._params['interval']](filter_value)
#             }
#         })