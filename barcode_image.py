from pyzbar.pyzbar import decode
from PIL import ImageGrab, Image


def decode_barcodes(frame):
    """
    Decodifica os códigos de barras em uma imagem.
    """
    decoded = decode(frame)
    return [barcode.data.decode("utf-8") for barcode in decoded]


def pega_imagem_clipboard():
    img = pega_imagem_do_clipboard()
    if not img:
        raise TypeError("Não tem imagem no clipboard")

    return img


def pega_imagem_do_clipboard():
    img = ImageGrab.grabclipboard()

    if isinstance(img, Image.Image):
        return img

    raise TypeError("Não tem imagem no clipboard")


def trata_img(img):

    largura, altura = img.size
    #print(f"Imagem size: {img.size}")
    nlargura = 1024
    naltura = int((altura / largura) * nlargura)

    img = img.resize((nlargura, naltura), resample=Image.LANCZOS)

    #img.save('img.jpg')
    return img


def extrair_codigo_barras(img):

    largura, altura = img.size
    img = trata_img(img)

    decoded_barcodes = decode_barcodes(img)

    if not decoded_barcodes:
        if largura < 640:
            raise TypeError("A imagem está muito pequena, tente aumentar um pouco")

        raise TypeError("Não localizou codigo de barras")

    return decoded_barcodes

