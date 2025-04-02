import random
import time
from ..logger_config import get_logger

logger = get_logger(__name__)


popular_sites = [
    "facebook.com",
    "vnexpress.net",
    "truyenqqto.com",
    "shopee.vn",
    "zalo.me",
    "24h.com.vn",
    "chatgpt.com",
    "dantri.com.vn",
    "coccoc.com",
    "thegioididong.com",
    "thuvienphapluat.vn",
    "kenh14.vn",
    "wikipedia.org",
    "tuoitre.vn",
    "xosodaiphat.com",
    "msn.com",
    "truyenfull.io",
    "instagram.com",
    "znews.vn",
    "nettruyenvie.com",
    "baomoi.com",
    "laodong.vn",
    "vietnamnet.vn",
    "thanhnien.vn",
    "vietjack.com",
    "truyenwikidich.net",
    "bongdaplus.vn",
    "truyenfull.bio",
    "cellphones.com.vn",
    "dienmayxanh.com",
    "voz.vn",
    "nhathuoclongchau.com.vn",
    "xoso.com.vn",
    "reddit.com",
    "canva.com",
    "cafef.vn",
    "nettruyenrr.com",
    "soha.vn",
    "fptshop.com.vn",
    "truyenyy.vip",
    "yahoo.com",
    "roblox.com",
    "openai.com",
    "minhngoc.net.vn",
    "toptruyentv.net",
    "lazada.vn",
    "animevietsub.page",
    "toptruyen28.net",
    "bachhoaxanh.com",
    "discord.com",
    "pinterest.com",
    "bongda.com.vn",
    "animevietsub.biz",
    "tinhte.vn",
    "nguoiquansat.vn",
    "tienphong.vn",
    "github.com",
    "goctruyentranhvui8.com",
    "gamek.vn",
    "loigiaihay.com",
    "thethao247.vn",
    "nld.com.vn",
    "garena.vn",
    "chotot.com",
    "xskt.com.vn",
    "cambridge.org",
    "tamanhhospital.vn",
    "nimo.tv",
    "vtv.vn",
    "mobilecity.vn",
    "telegram.org",
]

dkkd_sites = [
    "dangkykinhdoanh.gov.vn",
    "dichvuthongtin.dkkd.gov.vn",
    "dangkyquamang.dkkd.gov.vn",
    "hokinhdoanh.dkkd.gov.vn",
    "bocaodientu.dkkd.gov.vn",
    "bocaodientu.dkkd.gov.vn/egazette"
]

def simulate_browsing(driver, total=1, dkkd=False):
    sites = dkkd_sites if dkkd else popular_sites
    for _ in range(total):
        # Open each site in a new tab
        site = random.choice(sites)
        try:
            driver.execute_script(f"window.open('https://{site}', '_blank');") 
            driver.switch_to.window(driver.window_handles[-1]) 
            time.sleep(random.randint(4,8)/2)
            driver.close()
            driver.switch_to.window(driver.window_handles[1])         
            time.sleep(1)
            logger.info(f"History simulated for {site}")
        except Exception as e:
            logger.error(f"Error while processing simulate for site {site}: {e}")

