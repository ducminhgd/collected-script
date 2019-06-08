import functools


def method_dispatch(func):
    """Support single dispatch of a class's method
    """
    dispatcher = functools.singledispatch(func)
    def wrapper(*args, **kwargs):
        return dispatcher.dispatch(args[1].__class__)(*args, **kwargs)

    wrapper.register = dispatcher.register
    functools.update_wrapper(wrapper, func)
    return wrapper


class EventA:
    ...


class EventB:
    ...


class EventC:
    ...


class EventHandler:

    @method_dispatch
    def apply(self, event):
        print(f'Not implemented or not registered for {event.__class__.__name__}')

    @apply.register(EventA)
    def _(self, event: EventA):
        print(f'Hope this is EventA and result is {event.__class__.__name__}')

    @apply.register(EventB)
    def _(self, event: EventB):
        print(f'Hope this is EventB and result is {event.__class__.__name__}')


if __name__ == '__main__':
    a = EventA()
    b = EventB()
    c = EventC()
    eh = EventHandler()

    eh.apply(a)
    eh.apply(b)
    eh.apply(c)
