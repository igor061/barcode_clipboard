from abc import ABC


import re
from functools import cache

from digito_verficador import calcular_modulo10, calcular_modulo11


class ValidaBoletoFactory:

    @classmethod
    def cria_ValidaBoleto(cls, codigo_barras):
        try:
            return ValidaBoletosPagamentos(codigo_barras)
        except ValueError:
            pass

        try:
            return ValidaBoletoConvenio(codigo_barras)
        except ValueError:
            pass

        raise ValueError("Codigo de barras invalido")

    @classmethod
    def cria_lista_ValidaBoleto(cls, lista):
        resp = []
        for codigo_barras in lista:
            try:
                resp.append(cls.cria_ValidaBoleto(codigo_barras))
            except ValueError:
                pass

        return resp


class ValidaBoleto(ABC):
    POSICAO_DIGITO_VERIFICADOR = None
    TAMANHO_CODIGO_BARRAS = None
    #func_modulo = calcular_dac_modulo11

    def __init__(self, codigobarras):
        self.codigbarras = codigobarras

    def __class__(self):
        return self.__class__

    def __str__(self):
        return self.codigo_barras

    def __repr__(self):
        return self.codigo_barras

    @classmethod
    def clear(cls, codig_barras):
        return re.sub(r'\D', '', codig_barras)

    def calcular_dv_codigo_barras(self, codigo_barras):
        pos_dv = self.POSICAO_DIGITO_VERIFICADOR
        codigo_barras_sem_dv = codigo_barras[:pos_dv] + codigo_barras[pos_dv + 1:]
        return self.func_modulo(codigo_barras_sem_dv)

    def validar_codigo_barras(self, codigo_barras):
        codigo = codigo_barras
        if not codigo.isdigit() or len(codigo) != self.TAMANHO_CODIGO_BARRAS:
            raise ValueError("Código de barras inválido: tamanho ou caracteres incorretos")

        dv = self.calcular_dv_codigo_barras(codigo)
        if dv != codigo[self.POSICAO_DIGITO_VERIFICADOR]:
            raise ValueError(f"Código de barras inválido: dv errado {dv}")

        return True

    def montar_linha_digitavel(self):
        raise NotImplemented

    @staticmethod
    def linha_digitavel_para_codigo_barras(linha_digitavel):
        raise NotImplemented

    @staticmethod
    def lista_validaboletos_para_linha_digitavel(lista):

        return [valida_boleto.montar_linha_digitavel() for valida_boleto in lista]


class ValidaBoletosPagamentos(ValidaBoleto):
    TAMANHO_CODIGO_BARRAS = 44
    POSICAO_DIGITO_VERIFICADOR = 4

    def __init__(self, codigo_barras):
        self.func_modulo = calcular_modulo11
        codigo_barras = self.clear(codigo_barras)
        self.validar_codigo_barras(codigo_barras)
        self.codigo_barras = codigo_barras

    def validar_codigo_barras(self, codigo_barras):
        if codigo_barras[0] == '8':
            raise ValueError("Codigo de barras não pode começar com 8")

        super().validar_codigo_barras(codigo_barras)

    @cache
    def montar_linha_digitavel(self):
        # quebrar o código em campos
        codigo_barras = self.codigo_barras
        campo1, campo2, campo3, campo4, campo5 = (
            codigo_barras[0:3] + codigo_barras[3] + codigo_barras[19:24],
            codigo_barras[24:34],
            codigo_barras[34:44],
            codigo_barras[4],
            codigo_barras[5:9] + codigo_barras[9:19],
        )

        # calcular os dígitos verificadores
        dv1, dv2, dv3 = map(calcular_modulo10, [campo1, campo2, campo3])

        # formatar a linha digitável
        linha_digitavel = f"{campo1[:5]}.{campo1[5:9]}{dv1} {campo2[:5]}.{campo2[5:10]}{dv2} {campo3[:5]}.{campo3[5:10]}{dv3} {campo4} {campo5}"

        return linha_digitavel

    @classmethod
    def apartir_linha_digitavel(cls, linha_digitavel):
        # remove tudo que não é dígito da linha digitável
        ld = re.sub(r'\D', '', linha_digitavel)

        # separa os campos da linha digitável e monta o código de barras
        campos = [
            ld[0:4],
            ' ',
            ld[33:47],
            ld[4:9],
            ld[10:20],
            ld[21:31]
        ]
        cod_barras = ''.join(campos)

        # calcula o DV do código de barras e o insere na posição correta
        dv = cls.calcular_dv_codigo_barras(cod_barras)
        cod_barras = cod_barras[:4] + str(dv) + cod_barras[5:]

        return cls(cod_barras)

    @classmethod
    def lista_linha_digitavel_apartir_codigosdebarras_validos(cls, lista_barcodes):
        lista_linha_digitavel = []

        for barcode in lista_barcodes:
            try:
                barcode_linha_digitavel = ValidaBoletosPagamentos.montar_linha_digitavel()
                lista_linha_digitavel.append(barcode_linha_digitavel)

            except ValueError:
                continue
        return lista_linha_digitavel

    @classmethod
    def lista_codigo_barras_validos(cls, lista):
        lista_barcodes = []
        for barcodeData in lista:
            try:
                if cls.validar_codigo_barras(barcodeData):
                    lista_barcodes.append(barcodeData)
            except ValueError as ve:
                pass

        return lista_barcodes


class ValidaBoletoConvenio(ValidaBoleto):

    TAMANHO_CODIGO_BARRAS = 44
    POSICAO_DIGITO_VERIFICADOR = 3
    TIPO_VALOR_DICT = {
        '6': calcular_modulo10,
        '7': calcular_modulo10,
        '8': calcular_modulo11,
        '9': calcular_modulo11,
    }

    def __init__(self, codigo_barras):
        codigo_barras = self.clear(codigo_barras)
        self._define_tipo_modulo(codigo_barras)

        print(self.func_modulo.__name__)
        self.validar_codigo_barras(codigo_barras)
        self.codigo_barras = codigo_barras

    def validar_codigo_barras(self, codigo_barras):
        if codigo_barras[0] != '8':
            raise ValueError("Codigo barras não começa com 8")

        super().validar_codigo_barras(codigo_barras)

    def _define_tipo_modulo(self, codigo_barras):
        tipo_valor = codigo_barras[2]
        self.func_modulo = self.TIPO_VALOR_DICT[tipo_valor]

    def montar_linha_digitavel(self):
        cod_barras = self.codigo_barras
        campo1 = cod_barras[:11]
        campo2 = cod_barras[11:22]
        campo3 = cod_barras[22:33]
        campo4 = cod_barras[33:44]

        func = self.func_modulo
        #func = calcular_modulo10
        #print(func.__name__)
        dv1 = func(campo1)
        dv2 = func(campo2)
        dv3 = func(campo3)
        dv4 = func(campo4)

        linha = f"{campo1}-{dv1} {campo2}-{dv2} {campo3}-{dv3} {campo4}-{dv4}"
        return linha


def test07():
    numero = "9434517811"

    print(calcular_modulo10(numero) == '8')


def test06():
    codigo_barras = '03392930200001364009011772500000000004630101'
    #codigo_barras = '36494000000000099900000100014256800000030971'
    print(BoletosPagamentos.validar_codigo_barras(codigo_barras))


def test01():
    codigo_barras = '03392930200001364009011772500000000004630101'
    linha_digitavel = ValidaBoletosPagamentos(codigo_barras).montar_linha_digitavel()
    print(linha_digitavel)


def test02():
    codigo_barras = '03392930200001364009011772500000000004630101'
    print(ValidaBoletosPagamentos(codigo_barras))


def test03():
    linha_digitavel = "03399.01175 72500.000004 00046.301016 2 93020000136400"
    codigo_barras_ok = '03392930200001364009011772500000000004630101'
    print("Linha digitável:", linha_digitavel)
    boleto = ValidaBoletosPagamentos.apartir_linha_digitavel(linha_digitavel)
    print("Reposta da funcao:", boleto)
    print("Resposta correta: ", codigo_barras_ok)


def test4():
    ld = "36490.00019 00014.256804 00000.309716 4 00000000009990"
    ld = "03399.01175 72500.000004 00046.301016 2 93020000136400"

    print(BoletosPagamentos.linha_digitavel_para_codigo_barras(ld))


def teste5():
    ini = [
        '12341234 124312341243',
        '03392930200001364009011772500000000004630101',
        '03399.01175 72500.000004 00046.301016 2 93020000136400'
    ]

    print(ini)
    print()
    lista = BoletosPagamentos.lista_codigo_barras_validos(ini)
    print("Codigoa de barras validos:")
    print(lista)

    print("")
    print("Lista linha digitavel:")
    lista = BoletosPagamentos.lista_linha_digitavel_apartir_codigosdebarras_validos(ini)
    print(lista)


ini = [
    '12341234 124312341243',
    '03392930200001364009011772500000000004630101',
    '03399.01175 72500.000004 00046.301016 2 93020000136400',
    "84830000004065001622023030611261187705916133",
    "81770000000 01093659970 41131079703 00143370831"
]


def test10():
    cod_barras = ini[4]
    boleto = ValidaBoletoConvenio(cod_barras)
    print(boleto)
    print(boleto.montar_linha_digitavel())


def test09():
    print(ValidaBoletoFactory.cria_lista_ValidaBoleto(ini))


def test08():

    codigobarras = ini[4]
    print(type(ValidaBoletoFactory.cria_ValidaBoleto(codigobarras)))


if __name__ == '__main__':
    test01()
    #test02()
    #test03()
    #test4()
    #teste5()
    #test06()
    #test07()
    #test08()
    test10()
