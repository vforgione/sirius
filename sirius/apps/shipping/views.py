import json
from math import ceil

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from functions import shipping_optimization
from models import Order


def home(request):
    if 'zipcode' in request.GET:
        payload = {
            'zip': request.GET['zipcode'],
            'items': []
        }
        for i in xrange(1, 15):
            key_uid = 'sku%d' % i
            key_weight = 'weight%d' % i
            key_qty = 'qty%d' % i
            if len(request.GET[key_uid]):
                payload['items'].append({
                    'uid': request.GET[key_uid],
                    'weight': int(ceil(float(request.GET[key_weight]))),
                    'qty': int(request.GET[key_qty]) or 1
                })
        cheapest = shipping_optimization(payload)
        if not isinstance(cheapest, Order):
            return HttpResponse(
                content=json.dumps(cheapest),
                content_type='application/json',
                status=400
            )

    else:
        cheapest = None

    return render_to_response(
        'shipping/home.html', {'cheapest': cheapest}, context_instance=RequestContext(request)
    )


@csrf_exempt
def optimize(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except Exception, e:
            return HttpResponse(
                content=json.dumps({'error': e}),
                content_type='application/json',
                status=400
            )
        cheapest = shipping_optimization(data)
        if not isinstance(cheapest, Order):
            return HttpResponse(
                content=json.dumps(cheapest),
                content_type='application/json',
                status=400
            )
        return HttpResponse(
            content=json.dumps(cheapest.to_json()),
            content_type='application/json'
        )

    else:
        return HttpResponse(
            content=json.dumps({'error': 'illegal http method - only POST allowed'}),
            content_type='application/json',
            status=400
        )
