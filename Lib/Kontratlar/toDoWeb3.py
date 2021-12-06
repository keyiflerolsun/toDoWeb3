# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

compiler_versiyon = "0.5.0"

# ! Ne Yağtığın Hakkında Fikrin Yoksa Aşağıya Dokunma!

from solcx import install_solc, compile_files
from solcx.exceptions import SolcNotInstalled, SolcInstallationError
from pathlib import Path

dosya_adi    = Path(__file__).stem
dosya_dizini = Path(__file__).parent.resolve()

try:
    derlenmis_kontrat = compile_files(
        source_files    = [f"{dosya_dizini}/{dosya_adi}.sol"],
        output_values   = ["abi", "bin"],
        solc_version    = compiler_versiyon
    )
except (SolcNotInstalled, SolcInstallationError):
    install_solc(compiler_versiyon)
    derlenmis_kontrat = compile_files(
        source_files    = [f"{dosya_dizini}/{dosya_adi}.sol"],
        output_values   = ["abi", "bin"],
        solc_version    = compiler_versiyon
    )

ABI      = derlenmis_kontrat[f"{dosya_dizini}/{dosya_adi}.sol:{dosya_adi}"]['abi']
BYTECODE = derlenmis_kontrat[f"{dosya_dizini}/{dosya_adi}.sol:{dosya_adi}"]['bin']

kontrat_veri = {
    "isim"     : dosya_adi,
    "abi"      : ABI,
    "bytecode" : BYTECODE
}