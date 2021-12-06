# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from typing import Dict, List, Optional, Union
from web3.datastructures import AttributeDict

from web3 import Web3
from web3.exceptions import ContractLogicError

from Lib.Kontratlar.toDoWeb3 import kontrat_veri

from datetime import datetime
from pytz import timezone

tarih = lambda : datetime.now(timezone("Turkey")).strftime("%d-%m-%Y %X")

class AgHatasi(Exception):
    """İstenilen Ağa Bağlanılamadı"""
    pass

class KekikBSC:
    def __init__(self, private_key:str):
        """toDoWeb3 KekikBSC Sınıfı"""
        self.network_adi  = "BSC Testnet"
        self.rpc_url      = "https://data-seed-prebsc-1-s1.binance.org:8545"
        self.bsc_scan_url = "https://testnet.bscscan.com/tx/"
        self.chain_id     = 97

        self.web3 = Web3(Web3.HTTPProvider(self.rpc_url))

        if not self.web3.isConnected():
            raise AgHatasi(f'{self.rpc_url} | {self.network_adi} Ağına Bağlanılamadı..')

        self.private_key = private_key
        key_to_cuzdan    = self.web3.eth.account.privateKeyToAccount(private_key).address
        self.cuzdan      = self.web3.toChecksumAddress(key_to_cuzdan)

        self.kontrat_hex  = self.web3.toChecksumAddress("0x4DB6A3A9e71a9Cf35EaDa87877554874312E0FF2")
        kontrat_abi  = kontrat_veri['abi']
        self.kontrat = self.web3.eth.contract(address=self.kontrat_hex, abi=kontrat_abi)

    def _tx_detay(self, tx_hash:str) -> Dict[str, str]:
        """Verilen TX Hex'inin Detayını Döndürür"""
        return self.web3.eth.get_transaction(tx_hash)

    def _tx2log(self, tx_hash:str) -> AttributeDict:
        """Verilen TX Hex'inin Log Objesini Döndürür"""
        return self.web3.eth.getTransactionReceipt(tx_hash)['logs'][0]

    def gorev_olustur(self, gorev:str) -> Dict[str, Optional[str]]:
        """Verilen Görev'i Web3'e Ekler"""
        # Görev Oluştur TX'i
        gorev_olustur_tx = self.kontrat.functions.gorevOlustur(gorev).buildTransaction(
            {
                'from'  : self.cuzdan,
                'nonce' : self.web3.eth.getTransactionCount(self.cuzdan),
            }
        )

        # TX'i Private Key ile İmzala
        gorev_olustur_tx_olustur = self.web3.eth.account.signTransaction(gorev_olustur_tx, private_key = self.private_key)

        # TX Gönder ve Makbuz Bekle
        gorev_olustur_tx_hash_byte = self.web3.eth.sendRawTransaction(gorev_olustur_tx_olustur.rawTransaction)
        gorev_olustur_tx_makbuz    = self.web3.eth.waitForTransactionReceipt(gorev_olustur_tx_hash_byte)

        # TX Verileri
        tx_hash = gorev_olustur_tx_makbuz.transactionHash.hex()
        tx_log  = self._tx2log(tx_hash)

        event_args = dict(self.kontrat.events.GorevOlustur().processLog(tx_log).args)

        return {
            "tarih"      : tarih(),
            "olay"       : "GorevOlustur",
            "detay"      : event_args['icerik'],
            "tx_hash"    : tx_hash,
            "bsc_scan"   : self.bsc_scan_url + tx_hash,
            "event_args" : event_args
        }

    @property
    def _toplam_gorev_sayisi(self) -> int:
        """Kontrattaki Görev Sayısını Döndürür"""
        return self.kontrat.functions.gorev_sayisi().call()

    def gorev_getir(self, gorev_id:int) -> Dict[str, Union[str, int, bool]]:
        """İstenen Görev'in Bilgisini Döndürür"""
        gorev = self.kontrat.functions.gorevler(gorev_id).call()
        return {
            "cuzdan"     : gorev[0],
            "gorev_id"   : gorev[1],
            "icerik"     : gorev[2],
            "tamamlanma" : gorev[3]
        }

    @property
    def tum_gorevler(self) -> List[dict[str, Union[str, int, bool]]]:
        """Kontrattaki Bütün Görevlerin Bilgilerini Döndürür"""
        gorev_listesi =  [
            self.gorev_getir(say)
                for say in range(1, self._toplam_gorev_sayisi + 1)
        ]
        if gorev_listesi != []:
            return sorted(gorev_listesi, key=lambda sozluk: sozluk['tamamlanma'])
        else:
            return gorev_listesi

    @property
    def benim_gorevlerim(self) -> Optional[List[dict[str, Union[str, int, bool]]]]:
        """Sınıf'a Girilen Private Key'e Ait Cüzdanın Görevlerini Döndürür"""
        return [
            gorev
                for gorev in self.tum_gorevler
                    if gorev['cuzdan'] == self.cuzdan
        ]

    def gorev_tamamla(self, gorev_id:int) -> Dict[str, Optional[str]]:
        """Verilen Görev'in Tamamlanma Durumunu Değiştirir"""
        # Görev Tamamla TX'i
        try:
            gorev_tamamla_tx = self.kontrat.functions.gorevTamamla(gorev_id).buildTransaction(
                {
                    'from'  : self.cuzdan,
                    'nonce' : self.web3.eth.getTransactionCount(self.cuzdan),
                }
            )
        except ContractLogicError:
            return {"hata": f"ID {gorev_id} Size Ait Değil!"}

        # TX'i Private Key ile İmzala
        gorev_tamamla_tx_olustur = self.web3.eth.account.signTransaction(gorev_tamamla_tx, private_key = self.private_key)

        # TX Gönder ve Makbuz Bekle
        gorev_tamamla_tx_hash_byte = self.web3.eth.sendRawTransaction(gorev_tamamla_tx_olustur.rawTransaction)
        gorev_tamamla_tx_makbuz    = self.web3.eth.waitForTransactionReceipt(gorev_tamamla_tx_hash_byte)

        # TX Verileri
        tx_hash = gorev_tamamla_tx_makbuz.transactionHash.hex()
        tx_log  = self._tx2log(tx_hash)

        event_args = dict(self.kontrat.events.GorevTamamla().processLog(tx_log).args)

        return {
            "tarih"      : tarih(),
            "olay"       : "GorevTamamla",
            "detay"      : f"{event_args['gorev_id']} : {'✅' if event_args['tamamlanma'] else '❌'}",
            "tx_hash"    : tx_hash,
            "bsc_scan"   : self.bsc_scan_url + tx_hash,
            "event_args" : event_args
        }