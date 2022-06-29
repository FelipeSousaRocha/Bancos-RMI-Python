from Pyro5.api import Daemon, locate_ns  # Funcoes para conectar os bancos
import bancos

# Daemon para conectar os bancos
with Daemon() as daemon:
    with locate_ns() as ns:
        # Criar dois "links" diferentes para os bancos
        uri = daemon.register(bancos.Restrito)
        ns.register("example.bancos.Restrito", uri)
        uri = daemon.register(bancos.Irrestrito)
        ns.register("example.bancos.Irrestrito", uri)
        # Mostrar os bancos
        print("Bancos disponíveis:")
        print(list(ns.list(prefix="example.bancos.").keys()))

    # Entrar no circuito de serviço.
    print("Os bancos estão prontos para os clientes.")
    daemon.requestLoop()
