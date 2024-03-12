import sys

from mitmmock import MitmMock


class StderrStatesNotifier:
    def running(self):
        print('mitmmock running', file=sys.stderr)

    def request(self, flow):
        print(flow.request.get_state(), file=sys.stderr)


addons = [MitmMock(), StderrStatesNotifier()]
