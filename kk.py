z = ['12-345678 K 44',
	  '12-345678 K 67',
	 '12-345678 8 48',
	 '18 458947 J 87',
	 '18 458947 J $ 87',
	 '1234567899874646',
	 '22212078M22',
	 '23$34678M33',
	]


v = ['26377286^4976',
	'263771103904',
	'26377899944',
	'772976864',
	'772 976 864',
	'+263772976864',
	'7 7 2 9 7 6 864',
	]

def check_id_number(n):
    is_clean = True
    r = ''
    for p in n:
        if p not in [' ', '-']:
            r += p
    n = r
    r = ""
    for p in n:
        if p not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890':
            is_clean = False
        else:
            r += p
    n = r

    if len(r) == 11:
        if r[8] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            is_clean = False
        r = r[0:8] + r[9:12]
        for p in r:
            if p not in '1234567890':
                is_clean = False
    else:
        is_clean = False

    return is_clean, n


def check_mobile_number(n):
    is_clean = True
    r = ''
    for p in n:
        if p not in [' ', '+']:
            r += p

    n = r
    r = ''
    for p in n:
    	if p not in '1234567890':
    		is_clean = False
    	else: 
    		r += p
    n = r.lstrip('0')

    if n.find('263') != 0:
        n = '263' + n

    if len(n) == 12:
    	if n[0:5] not in ['26377', '26371', '26373']:
    		is_clean = False
    else:
    	is_clean =  False 
    return is_clean, n

print('Starting....')
for k in v:
	i, j =  check_mobile_number(k)
	res = "{} => {} : {}".format(k, str(i), j) 
	print(res)
