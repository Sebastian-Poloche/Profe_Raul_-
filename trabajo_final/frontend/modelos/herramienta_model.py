"""Modelo de datos para Herramienta en la capa de presentación."""


class Herramienta:
    """
    Representa una herramienta en la interfaz gráfica del frontend.
    
    Encapsula los atributos principales de una herramienta para su uso
    en la presentación al usuario.
    """

    def __init__(self, id, codigo, nombre, categoria):
        """
        Inicializa una nueva instancia de Herramienta.
        
        Args:
            id (int): Identificador único en la base de datos
            codigo (str): Código único de la herramienta (7 caracteres)
            nombre (str): Nombre descriptivo de la herramienta
            categoria (str): Categoría a la que pertenece
        """
        self.id = id
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria

    def __str__(self):
        """Representación en texto para logging y depuración."""
        return f"Herramienta({self.codigo} - {self.nombre})"

    def __repr__(self):
        """Representación oficial del objeto."""
        return f"Herramienta(id={self.id}, codigo={self.codigo}, nombre={self.nombre})"
