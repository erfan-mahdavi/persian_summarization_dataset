import multiprocessing
import pymysql
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.irna import IrnaSpider
from spiders.khabaronline import KhabaronlineSpider
from spiders.isna import IsnaSpider
from spiders.mehrnews import MehrnewsSpider
from spiders.tasnimnews import TasnimnewsSpider
from spiders.hamshahrionline import HamshahrionlineSpider
from spiders.digiato import DigiatoSpider
from spiders.gamefa_cinema import GamefaCinemaSpider
from spiders.gamefa_tech import GamefaTechSpider
from spiders.gamefa_expo import GamefaExpoSpider
from spiders.gamefa_platform import GamefaPlatformSpider
from spiders.gamefa import GamefaSpider
from spiders.digikala_art import DigikalaArtSpider
from spiders.digikala_cook import DigikalaCookSpider
from spiders.bazicenter_news import BazicenterNewsSpider
from spiders.bazicenter_articles import BazicenterArticlesSpider
from spiders.bazicenter_review import BazicenterReviewSpider
from spiders.dbazi_events import DbaziEventsSpider
from spiders.dbazi import DbaziSpider
from spiders.sargarme import SargarmeSpider
from spiders.vigiato import VigiatoSpider
from spiders.digikala_game import DigikalaGameSpider
from spiders.technolife import TechnolifeSpider
from spiders.digikala_tech import DigikalaTechSpider
from spiders.techrato import TechratoSpider
from spiders.varzesh3 import Varzesh3Spider
from spiders.tarafdari import TarafdariSpider
from spiders.khabarvarzeshi import KhabarvarzeshiSpider
from spiders.meydannews import MeydannewsSpider
from spiders.kayhanvarzeshi import KayhanvarzeshiSpider

def run_spider(spider_cls):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_cls)
    process.start()
    

def clear_all_tables():
    s = get_project_settings().getdict("MYSQL_SETTINGS")
    conn = pymysql.connect(**s)
    cursor = conn.cursor()
    spiders = [
        "irna","khabaronline","isna","mehrnews","tasnimnews","hamshahrionline",
        "digiato","gamefa_cinema","gamefa_tech","gamefa_expo","gamefa_platform",
        "gamefa","digikala_art","digikala_cook","bazicenter_news",
        "bazicenter_articles","bazicenter_review","dbazi_events","dbazi",
        "sargarme","vigiato","digikala_game","technolife","digikala_tech",
        "techrato","varzesh3","tarafdari","khabarvarzeshi","meydannews",
        "kayhanvarzeshi"
    ]
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    for name in spiders:
        cursor.execute(f"TRUNCATE TABLE `{name}_articles`;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    conn.close()


if __name__ == '__main__':
    clear_all_tables()
    spiders = [
        IrnaSpider,
        KhabaronlineSpider,
        IsnaSpider,
        MehrnewsSpider,
        TasnimnewsSpider,
        HamshahrionlineSpider,
        DigiatoSpider,
        GamefaCinemaSpider,
        GamefaTechSpider,
        GamefaExpoSpider,
        GamefaPlatformSpider,
        GamefaSpider,
        DigikalaArtSpider,
        DigikalaCookSpider,
        BazicenterNewsSpider,
        BazicenterArticlesSpider,
        BazicenterReviewSpider,
        DbaziEventsSpider,
        DbaziSpider,
        SargarmeSpider,
        VigiatoSpider,
        DigikalaGameSpider,
        TechnolifeSpider,
        DigikalaTechSpider,
        TechratoSpider,
        Varzesh3Spider,
        TarafdariSpider,
        KhabarvarzeshiSpider,
        MeydannewsSpider,
        KayhanvarzeshiSpider
    ]
    with multiprocessing.Pool(processes=len(spiders)) as pool:
        pool.map(run_spider, spiders)
