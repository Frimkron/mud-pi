from character import Character

class ExampleClass(Character):
    def cmd_echo(self, args):
        '''Echoes the provided phrase back.
        usage: example [phrase]
        '''
        self.message(args)