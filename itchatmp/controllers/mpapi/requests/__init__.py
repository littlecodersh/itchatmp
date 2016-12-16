from itchatmp.config import COROUTINE

# if you have itchatmphttp installed
# we will use coroutine requests instead
if COROUTINE:
    try:
        from itchatmphttp import requests
    except ImportError:
        raise ImportError('You must installed itchatmphttp to use coroutine features')
else:
    import requests
    requests.packages.urllib3.disable_warnings()
    requests = requests.session()
    requests.verify = False
