import memcache
memc = memcache.Client(['127.0.0.1:11211'])

memc.set('minh', 'hello')
print memc.get('minh')