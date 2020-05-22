msg_types = {'feelings'}

def feelings(request):
    request['status'] = 'parsed'
    return request