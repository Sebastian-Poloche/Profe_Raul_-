import requests

class Comunicacion():

    def __init__(self, root):
        self.url = 'http://127.0.0.1:8000/cargues/'
        self.root = root

    def guardar(self, placa_del_vehiculo, valor_del_cargue, tipo_de_carga, vencimiento_de_soat):
        try:
            print(f"Guardando: {placa_del_vehiculo}, {valor_del_cargue}, {tipo_de_carga}, {vencimiento_de_soat}")
            data = {
                'Placa_del_vehiculo': placa_del_vehiculo,
                'Valor_del_cargue': valor_del_cargue,
                'Tipo_de_carga': tipo_de_carga,
                'Vencimiento_de_soat': vencimiento_de_soat,
            }
            resultado = requests.post(self.url, json=data)
            print(f"Respuesta: {resultado.status_code}")
            return resultado
        except Exception as e:
            print(f"Error: {e}")
            return None

    def actualizar(self, id, placa_del_vehiculo, valor_del_cargue, tipo_de_carga, vencimiento_de_soat):
        try:
            print(f"Actualizando ID {id}: {placa_del_vehiculo}, {valor_del_cargue}, {tipo_de_carga}, {vencimiento_de_soat}")
            data = {
                'Placa_del_vehiculo': placa_del_vehiculo,
                'Valor_del_cargue': valor_del_cargue,
                'Tipo_de_carga': tipo_de_carga,
                'Vencimiento_de_soat': vencimiento_de_soat,
            }
            resultado = requests.put(self.url + str(id) + '/', json=data)
            print(f"Respuesta: {resultado.status_code}")
            return resultado
        except Exception as e:
            print(f"Error: {e}")
            return None

    def consultar(self, id):
        try:
            resultado = requests.get(self.url + str(id) + '/')
            return resultado.json()
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def consultar_todo(self, placa_del_vehiculo='', tipo_de_carga=''):
        try:
            url = self.url
            params = {}
            if placa_del_vehiculo != '':
                params['Placa_del_vehiculo'] = placa_del_vehiculo
            if tipo_de_carga != '':
                params['Tipo_de_carga'] = tipo_de_carga
            
            resultado = requests.get(url, params=params)
            return resultado.json()
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def eliminar(self, id):
        try:
            resultado = requests.delete(self.url + str(id) + '/')
            return resultado.status_code
        except Exception as e:
            print(f"Error: {e}")
            return None