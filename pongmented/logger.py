import logbook
import sys

log = logbook.Logger('PONG', level=logbook.DEBUG)
logbook.StreamHandler(sys.stdout).push_application()
