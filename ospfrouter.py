from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.cli import CLI
from mininet.log import setLogLevel

class DynamicRouter(Node):
    """Dinamik yönlendirme için yönlendirici düğüm"""

    def config(self, **params):
        super(DynamicRouter, self).config(**params)
        self.cmd('sysctl -w net.ipv4.ip_forward=1')  # IP yönlendirmeyi etkinleştir

    def terminate(self):
        self.cmd('sysctl -w net.ipv4.ip_forward=0')
        super(DynamicRouter, self).terminate()

class MyTopology(Topo):
    """Örnek topoloji: 3 yönlendirici ve her bir yönlendiriciye bağlı ana bilgisayarlar"""

    def build(self):
        # Yönlendiricileri tanımlama
        router1 = self.addNode('r1', cls=DynamicRouter)
        router2 = self.addNode('r2', cls=DynamicRouter)
        router3 = self.addNode('r3', cls=DynamicRouter)

        # Ana bilgisayarları tanımlama
        host1 = self.addHost('h1', ip='10.0.1.2/24', defaultRoute='via 10.0.1.1')
        host2 = self.addHost('h2', ip='10.0.2.2/24', defaultRoute='via 10.0.2.1')
        host3 = self.addHost('h3', ip='10.0.3.2/24', defaultRoute='via 10.0.3.1')

        # Yönlendirici ve ana bilgisayar bağlantıları
        self.addLink(host1, router1, intfName2='r1-eth0', params2={'ip': '10.0.1.1/24'})
        self.addLink(host2, router2, intfName2='r2-eth0', params2={'ip': '10.0.2.1/24'})
        self.addLink(host3, router3, intfName2='r3-eth0', params2={'ip': '10.0.3.1/24'})

        # Yönlendiriciler arası bağlantılar
        self.addLink(router1, router2, intfName1='r1-eth1', intfName2='r2-eth1', 
                     params1={'ip': '192.168.1.1/30'}, params2={'ip': '192.168.1.2/30'})
        self.addLink(router2, router3, intfName1='r2-eth2', intfName2='r3-eth1', 
                     params1={'ip': '192.168.2.1/30'}, params2={'ip': '192.168.2.2/30'})

def run():
    """Ağı başlat ve CLI aç"""
    topo = MyTopology()
    net = Mininet(topo=topo)
    net.start()

    # Quagga veya diğer yönlendirme protokollerini başlat
    routers = ['r1', 'r2', 'r3']
    for router in routers:
        r = net.get(router)
        r.cmd('zebra -f /etc/quagga/zebra.conf -d')
        r.cmd('ospfd -f /etc/quagga/ospfd.conf -d')  # OSPF dinamik yönlendirme protokolü

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
