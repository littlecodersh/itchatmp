import time, json
import functools, logging

logger = logging.getLogger('itchatmp')

def retry(n=3, waitTime=3):
    def _retry(fn):
        @functools.wraps(fn)
        def __retry(*args, **kwargs):
            for i in range(n):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    logger.debug('%s failed. Count: %s. Info: %r' %
                        (fn.__name__, i + 1, e))
                    if i + 1 == n:
                        logger.debug('%s failed. Reach max retry' %
                            fn.__name__)
                    time.sleep(waitTime)
        return __retry
    return _retry

def encode_send_dict(d):
    try:
        return json.dumps(d).encode('utf8'). \
            decode('unicode-escape').encode('utf8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return
