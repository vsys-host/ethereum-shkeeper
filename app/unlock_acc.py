import requests as rq

from .logging import logger
from .config import config

#global acc_password 
acc_password = False

    
def get_account_password():
    global acc_password 
    if acc_password:
        logger.warning("Get password from cache")
        return acc_password
    else:
        logger.warning("Get password from shkeeer")
        r = {
                "key": "shkeeper",
                "persistent_status": "enabled",
                "runtime_status": "success"
            }
#        r = rq.post(
#                        f'http://{config["SHKEEPER_HOST"]}/api/v1/USDT/decrypt',
#                        headers={'X-Shkeeper-Backend-Key': config['SHKEEPER_KEY']}
#                    )
        if r['persistent_status'] == "disabled":
            logger.warning('Encryption is disabled')
            acc_password =  r['key']
        elif r['persistent_status'] == "pending":
            logger.warning('Have not selected encryption mode yet')
            return False
        elif r['persistent_status'] == "enabled":
            if  r['runtime_status'] == "pending":
                logger.warning('Encryption enabled, but password is not entered yet')
                return False
            elif  r['runtime_status'] == "fail":
                logger.warning('Encryption enabled, but entered password is not correct')
                return False
            elif r["runtime_status"]== "success":
                acc_password = r['key']
            else:
                logger.warning(f'Receive unexpected response from shkeeper: {r.text}')       
        else:
            logger.warning(f'Receive unexpected response from shkeeper: {r.text}')
        
        return acc_password