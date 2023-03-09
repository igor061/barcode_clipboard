from unittest import TestCase

from digito_verificador import calcular_modulo11, calcular_modulo10


class TestCalcularModulor10(TestCase):
    def test_calcular_modulo10(self):
        assert calcular_modulo10('033990117') == '5'
        assert calcular_modulo10('0001425680') == '4'
        assert calcular_modulo10('0000030971') == '6'
        assert calcular_modulo10('9434517811') == '8'

    def test_calcular_modulo11(self):
        assert calcular_modulo11('0339930200001364009011772500000000004630101') == '2'
        assert calcular_modulo11('3649000000000099900000100014256800000030971') == '4'
        assert calcular_modulo11('84850000004') == '8'
        assert calcular_modulo11('06500162202') == '6'
        assert calcular_modulo11('30309112611') == '1'
        assert calcular_modulo11('87705916133') == '6'