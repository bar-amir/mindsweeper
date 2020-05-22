msg_types = {'depthImage'}

def depth_image(request):
    request['status'] = 'parsed'
    return None