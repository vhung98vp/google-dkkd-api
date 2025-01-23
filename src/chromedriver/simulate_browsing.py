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
    "onemount.com",
    "truyenqqto.com",
    "24h.com.vn",
    "msn.com",
    "dantri.com.vn",
    "coccoc.com",
    "truyenfull.io",
    "thegioididong.com",
    "vietnamnet.vn",
    "kenh14.vn",
    "soha.vn",
    "tuoitre.vn",
    "thanhnien.vn",
    "vov.vn",
    "vietnamplus.vn",
    "thuvienphapluat.vn",
    "masothue.com",
    "laodong.vn",
    "bongdaplus.vn",
    "canva.com",
    "cafef.vn"
]

dkkd_sites = [
    "dangkykinhdoanh.gov.vn",
    "dichvuthongtin.dkkd.gov.vn",
    "dangkyquamang.dkkd.gov.vn",
    "hokinhdoanh.dkkd.gov.vn",
    "bocaodientu.dkkd.gov.vn",
    "bocaodientu.dkkd.gov.vn/egazette"
]

def simulate_browsing(driver, total=1):
    for _ in range(total):
        # Open each site in a new tab
        site = random.choice(popular_sites)
        driver.execute_script(f"window.open('https://{site}', '_blank');") 
        driver.switch_to.window(driver.window_handles[-1]) 
        time.sleep(random.randint(4,8)/2)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])         
        time.sleep(1)
        logger.info(f"History simulated for {site}")


def simulate_dkkd(driver, total=1):
    driver.execute_script(f"window.open('https://{dkkd_sites[0]}', '_blank');") 
    driver.switch_to.window(driver.window_handles[-1]) 
    for _ in range(total):
        site = random.choice(dkkd_sites)
        time.sleep(random.randint(4,8)/2)
        driver.get(f"https://{site}") 
        logger.info(f"History simulated for {site}")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])