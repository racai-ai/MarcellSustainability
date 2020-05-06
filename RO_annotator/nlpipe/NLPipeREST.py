import platform
from multiprocessing import freeze_support
from http import HTTPStatus
from flask import Flask, request, send_from_directory
from flask_restful import Api, Resource
from NLPipe import NLPipe
from PipAlgo import PipAlgo

# Uses Flask-based Flask-RESTful api for creating the
# REST web service for the NLPipe platform.
# Author: Radu Ion (radu@racai.ro)
class NLPipeREST(Resource):
    """This is the REST web-service version of the NLPipe class.
    Just run this module and it will start the WS for you."""

    def __init__(self, *args):
        super().__init__()
        self._nlpipe = args[0]

    def post(self):
        """Returns the client key used for a
        config/processing request.
        Expected key=value pairs:
        <NLPipe operation>=<NLPipe NLP app> (0 or more)
        exec=<NLPipe operation>,<NLPipe operation>,... (0 or more)
        text=<text to be processed> (exactly 1)"""
        text = None

        # 1. Get the text for processing
        if 'text' in request.form:
            text = request.form['text']
        else:
            return ({
                'teprolin-conf': self._nlpipe.getConfiguration(),
                'teprolin-result': 'No text="..." field has been supplied!'},
                int(HTTPStatus.BAD_REQUEST))

        # 2. Do the requested configurations,
        # if such pairs exist
        noConfigRequested = True

        for op in PipAlgo.getAvailableOperations():
            if op in request.form:
                algo = request.form[op]

                try:
                    self._nlpipe.configure(op, algo)
                    noConfigRequested = False
                except RuntimeError as err:
                    return ({
                        'teprolin-conf': self._nlpipe.getConfiguration(),
                        'teprolin-result': str(err)},
                        int(HTTPStatus.BAD_REQUEST))

        # 2.1 If no configuration was requested,
        # go to the default configuration for the object.
        # Clear previous configuration requests.
        if noConfigRequested:
            self._nlpipe.defaultConfiguration()

        # 3. Extract the requested text processing
        # operations. If none is specified, do the full
        # processing chain.
        requestedOps = []

        if 'exec' in request.form:
            exop = request.form['exec'].split(",")

            for op in exop:
                if op in PipAlgo.getAvailableOperations():
                    requestedOps.append(op)
                else:
                    return ({
                        'teprolin-conf': self._nlpipe.getConfiguration(),
                        'teprolin-result': "Operation '" + op + "' is not recognized. See class PipAlgo."},
                        int(HTTPStatus.BAD_REQUEST))

        # 4. Do the actual work and return the JSON object.
        if requestedOps:
            dto = self._nlpipe.pcExec(text, requestedOps)
        else:
            dto = self._nlpipe.pcFull(text)

        return ({
            'teprolin-conf': self._nlpipe.getConfiguration(),
            'teprolin-result': dto.jsonDict()},
            int(HTTPStatus.OK))

class NLPipeApps(Resource):
    """Provides all of the available NLP apps that
    implement the given operation."""

    def __init__(self, *args):
        super().__init__()
        self._nlpipe = args[0]

    def get(self, oper):
        """This method will return the available NLPipe
        algorithms (NLP apps) for the specified 'oper'."""

        if oper in PipAlgo.getAvailableOperations():
            return ({oper: PipAlgo.getAlgorithmsForOper(oper)}, int(HTTPStatus.OK))
        else:
            return ({
                'teprolin-conf': self._nlpipe.getConfiguration(),
                'teprolin-result': "Operation '" + oper + "' is not recognized. See class PipAlgo."},
                int(HTTPStatus.BAD_REQUEST))

class NLPipeOperations(Resource):
    """Provides all of the available operations
    that NLPipe implements."""

    def __init__(self, *args):
        super().__init__()

    def get(self):
        """This method will return the available NLPipe
        operations (text annotators)."""

        return ({"can-do": PipAlgo.getAvailableOperations()}, int(HTTPStatus.OK))

class NLPipeTerminate(Resource):
    def __init__(self, *args):
        super().__init__()
        self._nlpipe = args[0]

    def get(self):
        """This method will gracefully shutdown
        the Flask server."""

        func = request.environ.get('werkzeug.server.shutdown')
        
        if func is not None:
            func()
        else:
            return ({
                'teprolin-conf': self._nlpipe.getConfiguration(),
                'teprolin-result': "Cannot shutdown server..."},
                int(HTTPStatus.FORBIDDEN))

# This is always used as a main module.
# Call freeze_support() first in Windows.
if platform.system() == "Windows":
    freeze_support()

# The NLPipe object.
# This one is configured and used
# for processing operations.
nlpipe = NLPipe()
app = Flask(__name__)
# Configure flask_restful to jsonify
# arbitrary objects.
app.config['RESTFUL_JSON'] = {
    'default': lambda x: x.__dict__,
    'ensure_ascii': False,
    'sort_keys': True,
    'indent': 2
}
api = Api(app)

# GET the available algorithms for the given operation
api.add_resource(
    NLPipeApps, '/apps/<string:oper>', resource_class_args=[nlpipe])
# GET the available operations for the platform
api.add_resource(NLPipeOperations, '/operations')
# POSTs the data for configuration and processing
api.add_resource(NLPipeREST, '/process', resource_class_args=[nlpipe])

# WARNING!
# If you run this with uwsgi, comment out the next 3 lines.
#api.add_resource(
#    NLPipeTerminate, '/server-shutdown-now', resource_class_args=[nlpipe])
#app.run(host = '127.0.0.1', port = 5000)
