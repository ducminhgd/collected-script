HANDLER_REGISTRY = {
    'hello': 'hello',
    'bye': 'bye',
}

class SayHanlder:

    def hello(self, name):
        print(f'Hello {name}!')

    def bye(self, name):
        print(f'Bye {name}')

    def say(self, event, name):
        handler_method = getattr(self, HANDLER_REGISTRY[event])
        handler_method(name)

sh = SayHanlder()
sh.say('hello', 'MinhGDD')