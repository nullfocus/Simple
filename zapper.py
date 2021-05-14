from flask import Flask, request
from functools import wraps
import os, logging, subprocess
from timeit import default_timer as timer

app = Flask(__name__)

def logged(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        log.debug(f.__name__)
        return f(*args, **kwargs)
    return decorated

def load_files():    
    return os.listdir(scripts_path)

def run_script(fullname):
    start = timer()

    fullname = str(fullname)

    output = ''


    if fullname.endswith('.py'):
        script_locals = {'args' : request.args, 'response' : '...'}

        with open(fullname) as file:
            exec(file.read(), None, script_locals)
        
        output = script_locals['response']
        
    else:
        output = subprocess.run([fullname], check=True, capture_output=True).stdout.decode("utf-8") 

    timespan = timer() - start

    return output, timespan

def page(title, content):
    return f'''
<html>
    <head>
        <title>{title}</title>
        <style>
            html, body, div, ul, li, a {{
                font-family: monospace;
                margin: 0;
                padding: 0;
                border: 0;
            }}

            html{{ font-size: 60%; padding: 1em;}}

            @media screen 
                and (min-width: 0px)
                and (max-width: 300px) 
            {{ html {{ font-size: 3.5em; }} }}

            @media screen 
                and (min-width: 301px)
                and (max-width: 600px) 
            {{ html {{ font-size: 3em; }} }}

            @media screen 
                and (min-width: 601px)
                and (max-width: 1000px) 
            {{ html {{ font-size: 2.5em; }} }}

            @media screen 
                and (min-width: 1001px)
            {{ html {{ font-size: 2em; }} }}

            ul{{ list-style: decimal; margin-left: 2em}}
        </style>
    </head>
    <body>
    {content}
    </body>
</html>
'''

@app.route('/')
@logged
def index():
    content = f'''
<div>available scripts:</div>
<ul>
'''

    for script in load_files():
        content += f'''
<li>
    <a 
        href="run?name={script}" 
        onclick="return confirm('Are you sure you want to execute {script}?')">
        
        {script}
    </a>
</li>
'''

    content += '</ul>'

    return page('scripts', content)

@app.route('/run')
@logged
def run():
    name = request.args.get('name')

    if name not in load_files():
        return '['+name+'] not found'

    fullname = scripts_path + name

    script_output, span = run_script(fullname)

    return page('output', f'''
<div>{fullname}</div>
<div>elapsed: {span}s</div>
<pre>{script_output}</pre>
''')

@app.route('/favicon.ico')
@logged
def favicon():
    return '', 404

#https://blog.sneawo.com/blog/2017/12/20/no-cache-headers-in-flask/
@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.errorhandler(Exception)
def all_exception_handler(error):
    log.debug(error)
    return 'Error', 500

if __name__ == '__main__':
    filepath = os.path.dirname(os.path.realpath(__name__))

    logfile_path = filepath + '/log.txt'
    scripts_path = filepath + '/scripts/'

    logging.basicConfig(level=logging.DEBUG, filename=logfile_path)
    log = logging.getLogger(os.path.basename(__file__))
    
    app.run(host='0.0.0.0', debug=True, port=5000)