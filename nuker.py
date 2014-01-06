#! /usr/bin/env python

import os.path
import argparse
import sh
import cmd

yeses = ['1', 'yes', 'y', 'true', 't']

def is_this_true (_s):
    _s = _s.strip().lower()
    if _s in yeses:
        return True
    return False

def find_files( cwd, pattern):
    sh.cd( cwd )
    output = sh.find( '.', '-name', find_name )
    arr = output.stdout.strip().split('\n')
    result = []
    for line in arr:
        result.append( line[2:] )
    return result

class DeleteCommand (cmd.Cmd):
    candidate = []
    deleting = []
    index = 0

    def set_list (self, _c):
        self.candidate = _c

    def preloop (self):
        self._display_item()

    def default (self, line):
        if is_this_true( line ):
            self.deleting.append( self.candidate[ self.index ] )
        self.index = self.index + 1
        if self.index >= len( self.candidate ):
            _exception = Exception('Done')
            _exception.deleting = self.deleting
            raise _exception
        self._display_item()

    def _display_item (self):
        self.prompt = 'Deleting "%s"? ' % self.candidate[ self.index ]

if __name__ == '__main__':
    parser = argparse.ArgumentParser( description='nuker allows you to clear files with the given suffix in your current working directory.' )
    parser.add_argument( 'suffix', type=str, nargs=1, help='suffix to delete' )

    args      = parser.parse_args()
    suffix    = args.suffix[0]
    cwd       = os.getcwd()
    find_name = '*.%s' % suffix
    found     = find_files( cwd, find_name )
    len_found = len( found )

    if len_found == 0:
        exit( 0 )

    cmd_d = DeleteCommand( completekey='Tab' )
    cmd_d.set_list( found )
    deleting_files = 0

    try:
        cmd_d.cmdloop()
    except KeyboardInterrupt:
        pass
    except Exception, e:
        if e.deleting:
            for item in e.deleting:
                try:
                    # print os.path.join( cwd, item )
                    os.unlink( os.path.join( cwd, item ) )
                    deleting_files = deleting_files + 1
                except Exception, e:
                    pass

    if deleting_files > 0:
        print "%d files are deleted." % (deleting_files)
    exit( 0 )

