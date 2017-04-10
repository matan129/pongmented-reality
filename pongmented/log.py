import sys
import logbook

logbook.StreamHandler(sys.stdout).push_application()
log = logbook.Logger('PONG', level=logbook.DEBUG)
