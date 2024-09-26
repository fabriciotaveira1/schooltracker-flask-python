from services.api_clima import ApiClima

class Registro:
    temperatura = None
    velocidade_do_vento = None
    umidade_do_ar = None
    def __init__(self, id_registro, id_viagem, data_registro, cidade, observacoes):
        self.id_registro = id_registro
        self.id_viagem = id_viagem
        self.data_registro = data_registro
        self.cidade = cidade
        self.observacoes = observacoes

    def registrar_dados_clima(self, api_clima,cidade):
        api_clima = ApiClima('da7d7856826a4e9daae192630241109')
        weather_data = api_clima.get_weather_data(cidade)
        if weather_data:
            self.temperatura = api_clima.get_temperature(cidade)
            self.velocidade_do_vento = api_clima.get_wind_velocity(cidade)
            self.umidade_do_ar = api_clima.get_humidity(cidade)

        
        