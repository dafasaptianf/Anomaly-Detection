from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import time

class MyTopo(Topo):
    def build(self):
        # Tambah 3 switch
        s1 = self.addSwitch('s1', cls=OVSKernelSwitch, protocols='OpenFlow13')
        s2 = self.addSwitch('s2', cls=OVSKernelSwitch, protocols='OpenFlow13')
        s3 = self.addSwitch('s3', cls=OVSKernelSwitch, protocols='OpenFlow13')

        # Tambah 6 host 
        h1 = self.addHost('h1', ip='10.0.0.1/24', mac='00:00:00:00:00:01')
        h3 = self.addHost('h3', ip='10.0.0.3/24', mac='00:00:00:00:00:03') # Attacker
        h4 = self.addHost('h4', ip='10.0.0.4/24', mac='00:00:00:00:00:04')
        h5 = self.addHost('h5', ip='10.0.0.5/24', mac='00:00:00:00:00:05')
        h6 = self.addHost('h6', ip='10.0.0.6/24', mac='00:00:00:00:00:06') # Attacker
        h7 = self.addHost('h7', ip='10.0.0.7/24', mac='00:00:00:00:00:07')

        # Sambungkan host ke switch
        self.addLink(h1, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        self.addLink(h5, s2)
        self.addLink(h6, s3)
        self.addLink(h7, s3)

        # Interkoneksi antar switch
        self.addLink(s1, s2)
        self.addLink(s2, s3)

def startNetwork():
    topo = MyTopo()
    # Hubungkan ke ONOS controller
    c0 = RemoteController('c0', ip='127.0.0.1', port=6653)
    net = Mininet(topo=topo, controller=c0, link=TCLink)

    print("Menjalankan jaringan dan menghubungkan ke controller...")
    net.start()

    print("Menunggu beberapa detik agar semua host dan switch siap...")
    time.sleep(3)

    print("Jalankan CLI Mininet. Coba periksa ping antar host dan topologi di ONOS.")
    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    startNetwork()
