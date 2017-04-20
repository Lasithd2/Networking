#assumptions- There are 3 buldings in the organization and a router for each buiding
                    #1 for the main building
                    #2 for the small building
                    #3 for the R and D,CEO and network departments



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
		defaultIP1 = '10.1.1.1/25'  # IP address for r1-eth1, for the small building
		router1 = self.addNode( 'r1', cls=LinuxRouter, ip=defaultIP1 )		

                defaultIP2 = '10.1.2.1/24'  # IP address for r2-eth1, for the main building
		router2 = self.addNode( 'r2', cls=LinuxRouter, ip=defaultIP2 )

		defaultIP3 = '10.1.3.1/25'  # IP address for r3-eth1, for the R and D,CEO and networking departments
		router3 = self.addNode( 'r3', cls=LinuxRouter, ip=defaultIP3 )

		
                #Hosts of the small building
		h1 = self.addHost( 'h1', ip='10.1.1.2/25', defaultRoute='via 10.1.1.1' )
		h2 = self.addHost( 'h2', ip='10.1.1.3/25', defaultRoute='via 10.1.1.1' )

		#Hosts of the main building
		h3 = self.addHost( 'h3', ip='10.1.2.2/24', defaultRoute='via 10.1.2.1' )
		h4 = self.addHost( 'h4', ip='10.1.2.3/24', defaultRoute='via 10.1.2.1' )

		#Hosts of the building with R&D,CEO and network departments

		#Hosts of R&D
		h5 = self.addHost( 'h5', ip='10.1.3.2/25' , defaultRoute='via 10.1.3.1')
		h6 = self.addHost( 'h6', ip='10.1.3.3/25' , defaultRoute='via 10.1.3.1')

		#Hosts of CEO
		h7 = self.addHost( 'h7', ip='10.1.4.2/25', defaultRoute='via 10.1.4.1' )
		h8 = self.addHost( 'h8', ip='10.1.4.3/25', defaultRoute='via 10.1.4.1' )

		#Hosts of network
		h9 = self.addHost( 'h9', ip='10.1.5.2/25', defaultRoute='via 10.1.5.1' )
		h10 = self.addHost( 'h10',ip='10.1.5.3/25', defaultRoute='via 10.1.5.1')

                #Adding switches for respective subnets
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')
		s3 = self.addSwitch('s3')
		s4 = self.addSwitch('s4')
		s5 = self.addSwitch('s5')

                #connecting hosts to respective switches of the subnets
		self.addLink(h1, s1)
		self.addLink(h2, s1)
		self.addLink(h3, s2)
		self.addLink(h4, s2)
		self.addLink(h5, s3)
		self.addLink(h6, s3)
		self.addLink(h7, s4)
		self.addLink(h8, s4)
            	self.addLink(h9, s5)
		self.addLink(h10,s5)
		
		
                #connecting switches to respective routers
		self.addLink( s1, router1, intfName2='r1-eth1', params2={ 'ip' : '10.1.1.1/25' })
		self.addLink( s2, router2, intfName2='r2-eth1', params2={ 'ip' : '10.1.2.1/24' })
		self.addLink( s3, router3, intfName2='r3-eth1', params2={ 'ip' : '10.1.3.1/25' })
		self.addLink( s4, router3, intfName2='r3-eth2', params2={ 'ip' : '10.1.4.1/25' })
		self.addLink( s5, router3, intfName2='r3-eth3', params2={ 'ip' : '10.1.5.1/25' })

                #connecting routers with each other
		self.addLink( router3, router2, intfName1='r3-eth4', params1={ 'ip' : '10.1.7.1/30' }, intfName2='r2-eth2', params2={ 'ip' : '10.1.7.2/30' })
                self.addLink( router2, router1, intfName1='r2-eth3', params1={ 'ip' : '10.1.6.1/30' }, intfName2='r1-eth2', params2={ 'ip' : '10.1.6.2/30' })

def run():
	"Test linux router"
	topo = NetworkTopo()
	net = Mininet( topo=topo )
	net.start()

        #creating routing table entries for router 3
	net[ 'r3' ].cmd( 'ip route add 10.1.2.0/24 via 10.1.7.2' )
	net[ 'r3' ].cmd( 'ip route add 10.1.1.0/25 via 10.1.7.2' )

        #creating routing table entries for router 2
	net[ 'r2' ].cmd( 'ip route add 10.1.3.0/25 via 10.1.7.1' )
	net[ 'r2' ].cmd( 'ip route add 10.1.4.0/25 via 10.1.7.1' )
	net[ 'r2' ].cmd( 'ip route add 10.1.5.0/25 via 10.1.7.1' )
	net[ 'r2' ].cmd( 'ip route add 10.1.1.0/25 via 10.1.6.2' )

        #creating routing table entries for router 1
	net[ 'r1' ].cmd( 'ip route add 10.1.2.0/24 via 10.1.6.1' )
	net[ 'r1' ].cmd( 'ip route add 10.1.3.0/26 via 10.1.6.1' )
	net[ 'r1' ].cmd( 'ip route add 10.1.4.0/29 via 10.1.6.1' )
	net[ 'r1' ].cmd( 'ip route add 10.1.5.0/29 via 10.1.6.1' )

	info( '*** Routing Table on Router0:\n' )
	print net[ 'r1' ].cmd( 'route' )

	info( '*** Routing Table on Router1:\n' )
	print net[ 'r2' ].cmd( 'route' )

	info( '*** Routing Table on Router1:\n' )
	print net[ 'r3' ].cmd( 'route' )

	CLI( net )
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )
	run()	





	


	

























		



