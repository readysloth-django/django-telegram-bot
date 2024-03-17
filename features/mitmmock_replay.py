import sys
import pickle
import base64

from mitmmock import MitmMock


class StderrStatesNotifier:
    def running(self):
        print('mitmmock running', file=sys.stderr)

    def request(self, flow):
        request = flow.request
        request_pickled = pickle.dumps(request)
        request_base64 = base64.b64encode(request_pickled).decode()
        print(request_base64, file=sys.stderr)

    def response(self, flow):
        response = flow.response
        response_pickled = pickle.dumps(response)
        response_base64 = base64.b64encode(response_pickled).decode()
        print(response_base64, file=sys.stderr)


addons = [MitmMock(), StderrStatesNotifier()]
