from services.api_clima import ApiClima

class Registro:
    def __init__(self, id_viagem, data_registro, cidade, observacoes,temperatura,velocidade_do_vento,umidade_do_ar):
        self.id_viagem = id_viagem
        self.data_registro = data_registro
        self.cidade = cidade
        self.observacoes = observacoes
        self.temperatura = temperatura
        self.velocidade_do_vento = velocidade_do_vento
        self.umidade_do_ar = umidade_do_ar



        
        