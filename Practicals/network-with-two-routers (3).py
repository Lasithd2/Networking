#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter( Node ):
	"A Node with IP forwarding enabled."

	def config( self, **params ):
		super( LinuxRouter, self).config( **params )
		# Enable forwarding on the router
		self.cmd( 'sysctl net.ipv4.ip_forward=1' )

	def terminate( self ):
		self.cmd( 'sysctl net.ipv4.ip_forward=0' )
		super( LinuxRouter, self ).terminate()

class NetworkTopo( Topo ):
	"A LinuxRouter"

	def build( self, **_opts ):
		defaultIP0 = '192.168.100.1/24'  # IP address for r0-eth1
		router0 = self.addNode( 'r0', cls=LinuxRouter, ip=defaultIP0 )

		defaultIP1 = '192.168.200.1/24'  # IP address for r1-eth1
		router1 = self.addNode( 'r1', cls=LinuxRouter, ip=defaultIP1 )


		h1 = self.addHost( 'h1', ip='192.168.100.2/24', defaultRoute='via 192.168.100.1' )
		h2 = self.addHost( 'h2', ip='192.168.100.3/24', defaultRoute='via 192.168.100.1' )
		h3 = self.addHost( 'h3', ip='192.168.200.2/24', defaultRoute='via 192.168.200.1' )

		# IMPORTANT: Why can't I add IP address 192.168.300.2 to this host as given in the question?
		h4 = self.addHost( 'h4', ip='192.168.250.2/24', defaultRoute='via 192.168.250.1' )

		s1 = self.addSwitch('s1')

		self.addLink(h1, s1)
		self.addLink(h2, s1)

		self.addLink( s1, router0, intfName2='r0-eth1', params2={ 'ip' : '192.168.100.1/24' } )
		self.addLink( h3, router1, intfName2='r1-eth1', params2={ 'ip' : '192.168.200.1/24' } )

		# IMPORTANT: Why can't I add IP address 192.168.300.1 to this router as given in the question?
		self.addLink( h4, router1, intfName2='r1-eth2', params2={ 'ip' : '192.168.250.1/24' } )

		# IMPORTANT: Look closely how I added the link details of both routers here.
		self.addLink( router0, router1, intfName1='r0-eth2', params1={ 'ip' : '192.168.251.1/24' }, intfName2='r1-eth3', params2={ 'ip' : '192.168.251.2/24' } )

def run():
	"Test linux router"
	topo = NetworkTopo()
	net = Mininet( topo=topo )
	net.start()

	# IMPORTANT: IP routing between different networks doesn't work if we don't make these routing table entries.
	net[ 'r0' ].cmd( 'ip route add 192.168.200.0/24 via 192.168.251.2' )
	net[ 'r0' ].cmd( 'ip route add 192.168.250.0/24 via 192.168.251.2' )
    net[ 'r1' ].cmd( 'ip route add 192.168.100.0/24 via 192.168.251.1' )

	info( '*** Routing Table on Router0:\n' )
	print net[ 'r0' ].cmd( 'route' )

	info( '*** Routing Table on Router1:\n' )
	print net[ 'r1' ].cmd( 'route' )

	CLI( net )
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	run()

