from __future__ import annotations

from typing import List, Dict

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.views.decorators.http import require_GET

from listings.models import Listing


def _listing_to_geo_dict(req: HttpRequest, obj: Listing) -> Dict:
    try:
        url = req.build_absolute_uri(reverse('new_listing_detail', args=[obj.id]))
    except Exception:
        url = ''
    return {
        'id': obj.id,
        'title': obj.title,
        'lat': obj.latitude,
        'lng': obj.longitude,
        'url': url,
        'city': obj.city,
        'state': obj.state,
        'deal_type': getattr(obj, 'deal_type', None),
        'price': obj.price,
        'original_url': getattr(obj, 'original_url', ''),
    }


@require_GET
def listings_geo(request: HttpRequest) -> JsonResponse:
    """Return published listings with coordinates and useful link fields.

    Optional query:
    - limit: max number of results (default 1000, max 5000)
    - bbox: "minLon,minLat,maxLon,maxLat" to spatially filter
    """
    qs = Listing.objects.filter(is_published=True).exclude(latitude__isnull=True).exclude(longitude__isnull=True)

    bbox = request.GET.get('bbox')
    if bbox:
        try:
            min_lon, min_lat, max_lon, max_lat = [float(x.strip()) for x in bbox.split(',')]
            qs = qs.filter(
                latitude__gte=min_lat,
                latitude__lte=max_lat,
                longitude__gte=min_lon,
                longitude__lte=max_lon,
            )
        except Exception:
            # ignore bad bbox
            pass

    try:
        limit = int(request.GET.get('limit', '1000'))
    except Exception:
        limit = 1000
    limit = max(1, min(limit, 5000))

    data = [_listing_to_geo_dict(request, obj) for obj in qs.order_by('-list_date')[:limit]]
    resp = JsonResponse({'count': len(data), 'results': data}, json_dumps_params={'ensure_ascii': False})
    resp['Access-Control-Allow-Origin'] = '*'
    return resp


@require_GET
def listing_geo_detail(request: HttpRequest, pk: int) -> JsonResponse:
    try:
        obj = Listing.objects.get(pk=pk, is_published=True)
        if obj.latitude is None or obj.longitude is None:
            return JsonResponse({'detail': 'Coordinates not available'}, status=404)
    except Listing.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)
    resp = JsonResponse(_listing_to_geo_dict(request, obj), json_dumps_params={'ensure_ascii': False})
    resp['Access-Control-Allow-Origin'] = '*'
    return resp


@require_GET
def openapi_spec(request: HttpRequest) -> JsonResponse:
    """Serve a minimal OpenAPI 3.1 spec describing this API."""
    spec = {
        'openapi': '3.1.0',
        'info': {
            'title': 'CoralCity Listings Geo API',
            'version': '1.0.0',
            'description': 'Public endpoints for listing coordinates and links (no auth).',
        },
        'paths': {
            '/api/listings': {
                'get': {
                    'summary': 'List listings with coordinates',
                    'parameters': [
                        {
                            'name': 'limit','in': 'query','schema': {'type': 'integer','minimum': 1,'maximum': 5000},
                            'description': 'Maximum results to return (default 1000)'
                        },
                        {
                            'name': 'bbox','in': 'query','schema': {'type': 'string'},
                            'description': 'minLon,minLat,maxLon,maxLat filter bounds'
                        },
                    ],
                    'responses': {
                        '200': {
                            'description': 'OK',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {
                                            'count': {'type': 'integer'},
                                            'results': {
                                                'type': 'array',
                                                'items': {'$ref': '#/components/schemas/ListingGeo'}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            '/api/listings/{id}': {
                'get': {
                    'summary': 'Get a listing by ID',
                    'parameters': [
                        {'name': 'id','in': 'path','required': True,'schema': {'type': 'integer'}}
                    ],
                    'responses': {
                        '200': {
                            'description': 'OK',
                            'content': {
                                'application/json': {
                                    'schema': {'$ref': '#/components/schemas/ListingGeo'}
                                }
                            }
                        },
                        '404': {'description': 'Not found'}
                    }
                }
            }
        },
        'components': {
            'schemas': {
                'ListingGeo': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'title': {'type': 'string'},
                        'lat': {'type': 'number','format': 'float'},
                        'lng': {'type': 'number','format': 'float'},
                        'url': {'type': 'string','format': 'uri'},
                        'city': {'type': 'string'},
                        'state': {'type': 'string'},
                        'deal_type': {'type': 'string'},
                        'price': {'type': 'integer'},
                        'original_url': {'type': 'string','nullable': True},
                    },
                    'required': ['id','lat','lng','url']
                }
            }
        }
    }
    resp = JsonResponse(spec)
    resp['Access-Control-Allow-Origin'] = '*'
    return resp
