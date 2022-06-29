from Pyro5.api import Daemon, locate_ns
import bancos


with Daemon() as daemon:
    with locate_ns() as ns:
        uri = daemon.register(bancos.Restrito)
        ns.register("example.bancos.Restrito", uri)
        uri = daemon.register(bancos.Irrestrito)
        ns.register("example.bancos.Irrestrito", uri)
        print("Bancos disponíveis:")
        print(list(ns.list(prefix="example.bancos.").keys()))

    # entrar no circuito de serviço.
    print("Os bancos estão prontos para os clientes.")
    daemon.requestLoop()
