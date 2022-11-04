a = {'col': 1, 'lin': 7}
b = {'col': 8, 'jurge': 7}

print(tuple(a.keys()))
if ('col', 'lin') == tuple(a.keys()):
    print('NIGGA')
else:
    print('BABU')
    
c = {'state': 'deez'}

if 'state' in c.keys():
    print('True')