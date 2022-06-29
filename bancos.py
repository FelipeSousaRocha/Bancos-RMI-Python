from Pyro5.api import expose, behavior


# Conta irrestrita.
class Conta(object):
    def __init__(self):
        self._saldo = 0.0

    def saque(self, quantia):
        self._saldo -= quantia

    def deposito(self, quantia):
        self._saldo += quantia

    def saldo(self):
        return self._saldo


# Conta de retirada restrita.
class ContaRestrita(Conta):
    def saque(self, quantia):
        if quantia <= self._saldo:
            self._saldo -= quantia
        else:
            raise ValueError('Saldo insuficiente')


# Banco abstrato.
@expose
@behavior(instance_mode="single")
class Banco(object):
    def __init__(self):
        self.contas = {}

    def nome(self):
        pass

    def criarConta(self, nome):
        pass

    def apagarConta(self, nome):
        try:
            del self.contas[nome]
        except KeyError:
            raise KeyError('Conta desconhecida')

    def deposito(self, nome, quantia):
        try:
            return self.contas[nome].deposito(quantia)
        except KeyError:
            raise KeyError('Conta desconhecida')

    def saque(self, nome, quantia):
        try:
            return self.contas[nome].saque(quantia)
        except KeyError:
            raise KeyError('Conta desconhecida')

    def saldo(self, nome):
        try:
            return self.contas[nome].saldo()
        except KeyError:
            raise KeyError('Conta desconhecida')

    def todasContas(self):
        cnts = {}
        for nome in self.contas.keys():
            cnts[nome] = self.contas[nome].saldo()
        return cnts


# Banco especial: Irrestrito. Tem contas irrestritas.
@expose
class Irrestrito(Banco):
    def nome(self):
        return 'Irrestrito'

    def criarConta(self, nome):
        if nome in self.contas:
            raise ValueError('Essa conta já existe')
        self.contas[nome] = Conta()


# Banco especial: Restrito. Tem contas restritas.
@expose
class Restrito(Banco):
    def nome(self):
        return 'Banco Restrito'

    def criarConta(self, nome):
        if nome in self.contas:
            raise ValueError('Essa conta já existe')
        self.contas[nome] = ContaRestrita()
