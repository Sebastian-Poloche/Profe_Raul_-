"""Modelo de datos para Préstamo en la capa de presentación."""


class Prestamo:
    """
    Representa un préstamo en la interfaz gráfica del frontend.
    
    Encapsula los atributos principales de un préstamo para su uso
    en la presentación al usuario.
    """

    def __init__(self, id, numero, herramienta, fecha, responsable):
        """
        Inicializa una nueva instancia de Préstamo.
        
        Args:
            id (int): Identificador único en la base de datos
            numero (str): Número único del préstamo (7 caracteres)
            herramienta (str): Código de la herramienta prestada
            fecha (str): Fecha del préstamo
            responsable (str): Persona responsable del préstamo
        """
        self.id = id
        self.numero = numero
        self.herramienta = herramienta
        self.fecha = fecha
        self.responsable = responsable

    def __str__(self):
        """Representación en texto para logging y depuración."""
        return f"Préstamo({self.numero} - {self.herramienta} a {self.responsable})"

    def __repr__(self):
        """Representación oficial del objeto."""
        return f"Prestamo(id={self.id}, numero={self.numero}, herramienta={self.herramienta})"

