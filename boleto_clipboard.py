import pyperclip
import subprocess
from plyer import notification

from barcode_image import decode_barcodes, pega_imagem_do_clipboard, extrair_codigo_barras
from validacao_boleto import ValidaBoletoFactory, ValidaBoleto


app_name = 'boleto_copia_cola'


def captura_area_e_salva_no_clipboard():
    subprocess.run(["SnippingTool.exe", "/clip"])


def salva_no_clipboard(texto):
    pyperclip.copy(texto)


def notifica_codigo_barras_no_clipboard(codigo_barras):
    notification.notify(
        title='Código de barras copiado',
        message=codigo_barras,
        app_name=app_name,
        app_icon=None,
        timeout=5,
    )


def notifica_erro(text):
    notification.notify(
        title='ERRO',
        message=text,
        app_name=app_name,
        app_icon=None,
        timeout=5,
        toast=True
    )


def valida_codigo_barras(decoded_barcodes):
    lista_barcodes = ValidaBoletoFactory.cria_lista_ValidaBoleto(decoded_barcodes)
    lista_linha_digitavel = ValidaBoleto.lista_validaboletos_para_linha_digitavel(lista_barcodes)

    if not lista_linha_digitavel:
        raise TypeError("Não localizou um código de barras válido")

    return lista_linha_digitavel[0]


try:
    captura_area_e_salva_no_clipboard()
    img = pega_imagem_do_clipboard()
    codigos_de_barras = extrair_codigo_barras(img)
    linha_digitavel = valida_codigo_barras(codigos_de_barras)
    # Deixa só os números
    linha_digitavel = ValidaBoleto.clear(linha_digitavel)

    salva_no_clipboard(linha_digitavel)
    notifica_codigo_barras_no_clipboard(linha_digitavel)

except TypeError as te:
    notifica_erro(str(te))
    raise te
