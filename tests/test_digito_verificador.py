import digito_verificador


def test_calcular_modulo11():
    assert digito_verificador.calcular_modulo11('1234567890') == '1'
    assert digito_verificador.calcular_modulo11('001905009') == '5'
    assert digito_verificador.calcular_modulo11('237900000002812326800000034400005018000535') == '3'
    assert digito_verificador.calcular_modulo11('34191747800000058771005542640000095805301400011') == '7'
