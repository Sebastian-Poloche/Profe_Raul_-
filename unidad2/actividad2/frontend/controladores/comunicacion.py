import requests

class Comunicacion():

    def __init__(self, root):
        # API endpoint: backend exposes the router at /api/projects/ (DRF router)
        self.url = 'http://localhost:8000/api/projects'
        self.root = root
        pass

    def guardar(self, placa_vehiculo, valor_cargue, tipo_carga, vencimiento_soat, numero_clase):
        try:
            print(placa_vehiculo, valor_cargue, tipo_carga)
            data = {
                # Use field names expected by the DRF serializer / model
                'Placa_del_vehiculo': placa_vehiculo,
                'Valor_del_cargue': valor_cargue,
                'Tipo_de_carga': tipo_carga,
                'Vencimiento_de_soat': vencimiento_soat,
                # numero_clase is not part of the current model; include only if backend expects it
                # 'numero_clase': int(numero_clase) if numero_clase is not None else None
            }
            resultado = requests.post(self.url + '/', json=data)
            # raise for HTTP errors to surface problems to the caller
            resultado.raise_for_status()
            try:
                return resultado.json()
            except ValueError:
                return resultado.text
        except Exception as e:
            # don't silently swallow exceptions — return or re-raise after logging
            print('Error en guardar():', e)
            raise
    
    def consultar(self, id):
        resultado = requests.get(self.url + '/' + str(id) + '/')
        resultado.raise_for_status()
        return resultado.json()
    
    def consultarTodo(self, placa, v_cargue, tipo_carga, soat, numero):
        params = {}
        # build query params only for provided filters
        if placa:
            params['Placa_del_vehiculo'] = placa
        if v_cargue:
            params['Valor_del_cargue'] = v_cargue
        if tipo_carga:
            params['Tipo_de_carga'] = tipo_carga
        if soat:
            params['Vencimiento_de_soat'] = soat
        if numero is not None:
            params['numero_clase'] = numero

        print(self.url + '/', params)
        resultado = requests.get(self.url + '/', params=params)
        resultado.raise_for_status()
        return resultado.json()