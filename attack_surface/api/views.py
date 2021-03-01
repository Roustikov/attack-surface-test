from django.http import JsonResponse, HttpResponseServerError
from api.models import VM
from neomodel import Traversal, INCOMING
from collections import OrderedDict
import logging


def attack(request):
    result = OrderedDict()
    try:
        vm_id = request.GET.get('vm_id', '')
        vm = VM.nodes.first_or_none(vm_id=vm_id)
        if vm is None:
            return JsonResponse([], safe=False)
        definition = dict(
            node_class=VM, direction=INCOMING, relation_type=None, model=None)
        incoming_traversal = Traversal(vm, VM.__label__, definition)
        all_incoming_vms = incoming_traversal.all()
    except Exception as e:
        logging.error(f'An error occured in /attack method: {e}')
        return HttpResponseServerError(['An error occured in /attack method.'])

    for incoming_vm in all_incoming_vms:
        result[incoming_vm.vm_id] = incoming_vm
    return JsonResponse(list(result.keys()), safe=False)


def stats(request):
    node_count = len(VM.nodes)
    request_count = request.middleware_response_count
    avg_request_time = request.middleware_avg_response_time
    return JsonResponse({
        "vm_count": node_count,
        "request_count": request_count,
        "average_request_time": avg_request_time}, safe=False)
