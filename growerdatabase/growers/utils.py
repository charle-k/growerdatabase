from urllib.request import urlopen
from urllib.parse import quote
import json

from django.conf import settings


from .models import Grower, District, IdGenerator, SmsQueue


def check_record_size(f):
    errors = []
    fdata = f.read()
    if isinstance(fdata, bytes):
        fdata = fdata.decode('utf-8')
    contents = fdata.splitlines()
    cleaned_records = []
    count = 0
    for l in contents:
        l = l.strip()
        count += 1
        fields = str(l).split(',')
        t = 0
        while t < len(fields):
            fields[t] = fields[t].strip().title()
            t += 1

        fields = list([_f for _f in fields if _f])
        if len(fields) == 5:
            fields[2] = fields[2].upper()
            fields[3] = fields[3].title()
            fields[4] = fields[4].title()
            fields.insert(0, count)
            cleaned_records.append(fields)
        else:
            errors.append([count,
             'Line does not have the requisite number of fields'])

    return cleaned_records, errors


def check_data_integrity(records, errors):
    districts = get_districts()
    cleaned_records = []

    for rec in records:
        is_clean = True
        if len(rec[1]) > 200:
            is_clean = False
            errors.append([rec[0],
             'The name is too long'])
        z, rec[2] = check_id_number(rec[2])
        if not z:
            is_clean = False
            errors.append([rec[0],
             'The ID Number is invalid'])

        z, rec[3] = check_mobile_number(rec[3])
        if not z:
            is_clean = False
            errors.append([rec[0],
             'Please check cellphone number'])

        dkey = rec[4] + rec[5]
        if dkey not in list(districts.keys()):
            errors.append([rec[0],
         'Check Province, District name, and if district is in that Province'])
            is_clean = False
        if is_clean:
            cleaned_records.append(rec)
    return  cleaned_records, errors, districts


def check_id_number(n):
    is_clean = True
    r = ''
    for p in n:
        if p not in (' ', '-'):
            r += p

    n = r
    r = ''
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


def get_districts():
    districts = District.objects.all()
    places = dict()
    for d in districts:
        dkey = d.get_key()
        places[dkey] = d
    return places


def check_mobile_number(n):
    is_clean = True
    r = ''
    for p in n:
        if p not in (' ', '+'):
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
        if n[0:5] not in ('26377', '26371', '26373'):
            is_clean = False
    else:
        is_clean = False
    return is_clean, n


def check_duplicate_id_numbers(records, errors):
    cleaned_records = []
    # errors = []
    ids = {}
    for rec in records:
        if rec[2] in list(ids.keys()):
            err = 'Duplicate ID Number in with line' + str(ids[rec[2]])
            errors.append([rec[0], err])
        else:
            ids[rec[2]] = rec[0]
            cleaned_records.append(rec)
    return cleaned_records, errors


def check_grower_existence(records, errors):
    cleaned_records = []

    for rec in records:
        if Grower.objects.filter(National_ID=rec[2]).exists():
            err = 'ID Number for ' + rec[1] + ' is already in the database'
            errors.append([rec[0], err])
        else:
            cleaned_records.append(rec)

    return records, errors


def create_records(records, errors, districts):
    count = 0
    for rec in records:
        idgen = IdGenerator(id_number=rec[2])
        grower = Grower(Grower_Name=rec[1],
                        National_ID=rec[2],
                        Mobile_Number=rec[3]
                        )

        grower.Grower_Number = idgen.get_id()
        dkey = rec[4] + rec[5]
        grower.District = districts[dkey]
        try:
            grower.save()
            count += 1
            create_sms(grower.Mobile_Number, grower.Grower_Name,
                      grower.Grower_Number)
        except:
            err = "Unable to create " + rec[1] + "'s record"
            errors.append([rec[0], err])
    return errors, count


def create_sms(cellphone, grower_name, grower_number):
    msg = 'Hie ' + grower_name
    msg += "\nYour Grower Account has been created. Your Grower"
    msg += " Number is " + grower_number
    sms = SmsQueue(cellphone=cellphone, message=msg)
    sms.save()


def get_sms_balance():
    ws_str = settings.BULKSMSWEB_URL + "&u=" + settings.BULKSMSWEB_USERNAME
    ws_str += "&h=" + settings.BULKSMSWEB_TOKEN + "&op=cr"
    http_response = urlopen(ws_str, timeout=30).read()
    data = json.loads(http_response.decode())
    try:
        bal = int(data['credit'])
    except:
        bal = 0
    try:
        error = int(data['error'])
    except:
        error = 0
    return bal, error, data['error_string']


def send_sms(destination, message):
    # send via BulkSMS HTTP API
    ws_str = settings.BULKSMSWEB_URL + "&u=" + settings.BULKSMSWEB_USERNAME
    ws_str += "&h=" + settings.BULKSMSWEB_TOKEN + "&op=pv"
    ws_str = ws_str + "&to=" + quote(destination) + "&msg=" + quote(message)
    """
    if settings.DEBUG:
        print(('\nDEBUG MODE -> ' + ws_str[0:300]))
        return 4444, ''
    else:
        http_response = urlopen(ws_str, timeout=30).read()
        data = json.loads(http_response.decode())
        return data['timestamp'], data['error_string']
    """
    http_response = urlopen(ws_str, timeout=30).read()
    data = json.loads(http_response.decode())
    return data['timestamp'], data['error_string']



def sms_queue():
    msgs = SmsQueue.objects.filter(
                        is_sent=False)[0:settings.BULKSMSWEB_BATCH_SIZE]
    err = ""
    for msg in msgs:
        t, err = send_sms(msg.cellphone, msg.message)
        if err:
            break
        msg.is_sent = True
        msg.save()

    return err





