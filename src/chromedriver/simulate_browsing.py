import random
import time
from ..logger_config import get_logger

logger = get_logger(__name__)


popular_sites = [
    "vnexpress.net",      
    "zalo.me",            
    "shopee.vn",          
    "dienmayxanh.com",  
    "viettel.com.vn",     
    "fpt.com.vn",         
    "vingroup.net",       
    "momo.vn",            
    "baomoi.com",         
    "tiki.vn",            
    "vinmec.com",         
    "vietjetair.com",
    "benhvienk.vn", 
    "vtv.vn",             
    "congcaphe.com",       
    "khanggia.com",    
    "bigc.vn",  
    "vnews.gov.vn",         
    "vnpt.com.vn",        
    "onemount.com"         
]

def simulate_browsing(driver, total):
    for _ in total:
        # Open each site in a new tab
        site = random.choice(popular_sites)
        driver.execute_script(f"window.open('https://{site}', '_blank');") 
        driver.switch_to.window(driver.window_handles[-1]) 
        time.sleep(5)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])         
        time.sleep(1)
        logger.info(f"History simulated for {site}")