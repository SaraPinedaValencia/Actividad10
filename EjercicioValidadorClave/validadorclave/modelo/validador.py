# TODO: Implementa el código del ejercicio aquí

from abc import ABC, abstractmethod
import re

from EjercicioValidadorClave.validadorclave.modelo.errores import NoTienePalabraSecretaError, NoTieneNumeroError, \
    NoCumpleLongitudMinimaError, NoTieneLetraMayusculaError, NoTieneLetraMinusculaError, NoTieneCaracterEspecialError


class ReglaValidacion(ABC):
    def __init__(self, longitud_esperada: int):
        self._longitud_esperada: int = longitud_esperada

    @abstractmethod
    def es_valida(self, clave: str):
        pass

    def _validar_longitud(self, clave: str) -> bool:
        return len(clave) > self._longitud_esperada

    @staticmethod
    def _contiene_mayuscula(clave: str) -> bool:
        return any(c.isupper() for c in clave)

    @staticmethod
    def _contiene_minuscula(clave: str) -> bool:
        return any(c.islower() for c in clave)

    @staticmethod
    def _contiene_numero(clave: str) -> bool:
        return any(c.isdigit() for c in clave)


class ReglaValidacionGanimedes(ReglaValidacion):
    def __init__(self):
        super().__init__(8)

    def es_valida(self, clave):
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError("La clave debe tener más de 8 caracteres.")
        if not self._contiene_mayuscula(clave):
            raise NoTieneLetraMayusculaError("La clave debe tener al menos una letra mayúscula.")
        if not self._contiene_minuscula(clave):
            raise NoTieneLetraMinusculaError("La clave debe tener al menos una letra minúscula.")
        if not self._contiene_numero(clave):
            raise NoTieneNumeroError("La clave debe tener al menos un número.")
        if not self._contiene_caracter_especial(clave):
            raise NoTieneCaracterEspecialError("La clave debe tener al menos un caracter especial (@, _, #, $, %).")
        return True

    @staticmethod
    def _contiene_caracter_especial(clave):
        return any(c in '@_#$%' for c in clave)


class ReglaValidacionCalisto(ReglaValidacion):
    def __init__(self):
        super().__init__(6)

    def es_valida(self, clave):
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError("La clave debe tener más de 6 caracteres.")
        if not self._contiene_numero(clave):
            raise NoTieneNumeroError("La clave debe tener al menos un número.")
        if not self._contiene_calisto(clave):
            raise NoTienePalabraSecretaError(
                "La clave debe tener la palabra 'calisto' escrita con al menos dos letras en mayúscula, pero no todas.")
        return True

    @staticmethod
    def _contiene_calisto(clave):
        calisto = clave.lower().find('calisto')
        if calisto == -1:
            return False
        else:
            calisto_mayusculas = sum(1 for c in clave[calisto:calisto + 7] if c.isupper())
            return 2 <= calisto_mayusculas < 7


class Validador:
    def __init__(self, regla):
        self._regla = regla

    def es_valida(self, clave):
        return self._regla.es_valida(clave)
