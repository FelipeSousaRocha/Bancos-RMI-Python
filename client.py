# Client Banco

from Pyro5.api import locate_ns, Proxy


# Um cliente do banco.
class Cliente(object):
    def __init__(self, nome):
        self.nome = nome

    def Negociar(self, bancos):
        print("\n*** %s está fazendo negócios com %s:" %
              (self.nome, bancos.nome()))
        print("Criando conta")
        try:
            bancos.criarConta(self.nome)
        except ValueError as x:
            print("Falha: %s" % x)
            print("Removendo conta e tentando novamente")
            bancos.apagarConta(self.nome)
            bancos.criarConta(self.nome)

        print("Depositar dinheiro R$200,00")
        bancos.deposito(self.nome, 200.00)
        print("Depositar dinheiro R$500,75")
        bancos.deposito(self.nome, 500.75)
        print("Saldo = %.2f" % bancos.saldo(self.nome))
        print("Retirar dinheiro (pix) R$400,00")
        bancos.saque(self.nome, 400.00)
        print("Saldo final = %.2f" % bancos.saldo(self.nome))


ns = locate_ns()


# lista os bancos disponíveis procurando no NS o caminho de prefixo fornecido
nomesBancos = [nome for nome in ns.list(prefix="example.bancos.")]
if not nomesBancos:
    raise RuntimeError('Não há bancos para fazer negócios!')

bancos = []  # lista de bancos (proxies)
print()
for nome in nomesBancos:
    print("Contatando o banco: %s" % nome)
    uri = ns.lookup(nome)
    bancos.append(Proxy(uri))


# Diferentes clientes que fazem negócios com todos os bancos
felipe = Cliente('Felipe')
matheus = Cliente('Matheus')

for banco in bancos:
    felipe.Negociar(banco)
    matheus.Negociar(banco)


# Lista todas as contas
print()
for banco in bancos:
    print("As contas no %s:" % banco.nome())
    contas = banco.todasContas()
    for nome in contas.keys():
        print("  %s : %.2f" % (nome, contas[nome]))
