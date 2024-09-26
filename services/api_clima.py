import requests

class ApiClima:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1/current.json?key={api_key}&q={cidade}"
    
    # Método para buscar os dados do clima
    def get_weather_data(self, cidade):
        try:
            response = requests.get(self.base_url.format(api_key=self.api_key, cidade=cidade))
            response.raise_for_status()  # Gera exceção para códigos de erro HTTP
            return response.json()  # Retorna os dados JSON
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão: {e}")
            return None
        except ValueError:
            print("Erro ao decodificar a resposta JSON")
            return None

    # Método para buscar a temperatura
    def get_temperature(self, cidade):
        weather_data = self.get_weather_data(cidade)
        if weather_data:
            return weather_data['current']['temp_c']
        return None

    # Método para buscar a velocidade do vento
    def get_wind_velocity(self, cidade):
        weather_data = self.get_weather_data(cidade)
        if weather_data:
            return weather_data['current']['wind_kph']
        return None

    # Método para buscar o país
    def get_country(self, cidade):
        weather_data = self.get_weather_data(cidade)
        if weather_data:
            return weather_data['location']['country']
        return None

    # Método para buscar a umidade
    def get_humidity(self, cidade):
        weather_data = self.get_weather_data(cidade)
        if weather_data:
            return weather_data['current']['humidity']
        return None
