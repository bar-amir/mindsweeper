msg_types = {'pose'}

def pose(request):
    request['status'] = 'parsed'
    return request