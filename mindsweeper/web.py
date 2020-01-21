import http.server
import pathlib
import datetime
from .website import Website

web_server = Website()
users = []

@web_server.route('/')
def index():
    global datapath
    global users
    for d in data_path.iterdir():
        user_id = d.stem
        users += user_id
    _INDEX_HTML = '''
    <html>
        <head>
            <title>Brain Computer Interface</title>
        </head>
        <body>
            <ul>
                {users}
            </ul>
        </body>
    </html>
    '''
    _USER_LINE_HTML = '''
    <li><a href="/users/{user_id}">user {user_id}</a></li>
    '''
    users.sort()
    users_html = []
    for u in users:
        users_html.append(_USER_LINE_HTML.format(user_id=u))
    index_html = _INDEX_HTML.format(users='\n'.join(users_html))
    data = index_html
    return 200, data


@web_server.route('/users/([0-9]+)')
def user(user_id):
    global data_path
    global users
    if user_id not in users:
        return 404, ''
    else:
        thoughts = []
        user_dir = data_path/user_id
        for f in user_dir.iterdir():
            dt = datetime.datetime.strptime(f.stem, '%Y-%m-%d_%H-%M-%S')
            content = open(f).read()
            thoughts.append([dt, content])
        _THOUGHTS_HTML = '''
        <html>
            <head>
                <title>Brain Computer Interface: User {user_id}</title>
            </head>
            <body>
                <table>
                    {thoughts}
                </table>
            </body>
        </html>
        '''
        _THOUGHT_LINE_HTML = '''
        <tr>
            <td>{dt}</td>
            <td>{thought}</td>
        </tr>
        '''
        thought_html = []
        for t in thoughts:
            thought_html.append(_THOUGHT_LINE_HTML.format(dt=t[0], thought=t[1]))
        thoughts_html = _THOUGHTS_HTML.format(user_id=user_id, thoughts='\n'.join(thought_html))
        data = thoughts_html
        return 200, data

def parse_address(address):
    res = address.split(":")
    res[1] = int(res[1])
    return tuple(res)

def run_webserver(address, data_dir):
    global data_path
    data_path = pathlib.Path(data_dir)
    web_server.run(address)

def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>')
        return 1
    try:
        run_webserver(parse_address(argv[1]), argv[2])
    except Exception as error:
        print(f'ERROR: {error}')
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
