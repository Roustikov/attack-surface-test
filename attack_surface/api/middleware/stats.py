from timeit import default_timer as timer


class StatsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.avg_response_time = 0

    def __call__(self, request):
        start = timer()
        request.middleware_avg_response_time = self.avg_response_time
        request.middleware_response_count = self.request_count
        response = self.get_response(request)
        end = timer()

        self.avg_response_time = (self.avg_response_time + end - start)/2
        self.request_count += 1

        return response
