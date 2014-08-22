#!/usr/bin/env python

import sys
from config import default_parameters
from stream import Session

def parse_args():
    args = [sys.argv[i].lower() for i in range(len(sys.argv))]
    if '--debug' in args:
        default_parameters['DEBUG'] = True
    return default_parameters

def main():
    args = parse_args()
    if args['DEBUG']:
        from stream.process import Streamer
        from stream.util import join_threads
        streamer = Streamer()
        streamer.run(args['DEBUG'])
        try:
            join_threads(streamer.threads)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt caught.")
            print("Terminate main thread.")
            print("If only daemonic threads are left, terminate whole program.")
        finally:
            Session.remove()
    else:
        from stream.ui import app, MainWindow
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()