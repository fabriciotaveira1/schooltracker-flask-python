class Registro:
    def __init__(self, id_registro, id_viagem, data_hora_registro, cidade, observacoes, temperatura, velocidade_do_vento, umidade_do_ar, localizacao=None):
        self.id_registro = id_registro
        self.id_viagem = id_viagem
        self.data_hora_registro = data_hora_registro
        self.cidade = cidade
        self.observacoes = observacoes
        self.temperatura = temperatura
        self.velocidade_do_vento = velocidade_do_vento
        self.umidade_do_ar = umidade_do_ar
        self.localizacao = localizacao  # Se não for passado, será None
