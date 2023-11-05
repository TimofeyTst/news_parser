from abc import ABC, abstractmethod


class Parser(ABC):
    TICKERS = "SNPMF PCCYF XOM AMZN GOOGL MSFT META TSM INTC QCOM MAR HLT H BKNG ABNB TRVG BMWYY VLVLY F MBGYY POAHY CVS UNH MCK AAPL DIS CMCSA NFLX T SONY PARA FOX LVMHF ADDYY IDEXY NSRGY HSY DANOY WMT TGT WBA COST GE BA EADSY LMT CAT TSLA IBM TOSYY CSCO NVDA AMD"

    def __init__(self, session, callback):
        self.headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.1.906 (beta) Yowser/2.5 Safari/537.36",
            "accept-language": "ru,en;q=0.9,ba;q=0.8",
        }
        self.session = session
        self.callback = callback

    @abstractmethod
    async def fetch_and_parse(self, src, cat, supcat, url):
        pass
