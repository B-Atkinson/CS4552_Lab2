#!/usr/bin/env python

"""
Create a network where different switches are connected to
different controllers, by creating a custom Switch() subclass.
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.util import dumpNodeConnections


class Lab1(Topo):
    '''The topology from Lab 1 with switches [A,A2,B,C,D,E,F], two hosts [H1, H2], and an SDN controller connected to switch D.'''
    def build(self):
        net = Mininet( topo=None, build=False)
        
        # Add hosts
        leftHost = net.addHost( 'h1' )
        rightHost = net.addHost( 'h2' )
        
        # Add switches
        switchA = net.addSwitch( 'A' )
        switchA2 = net.addSwitch( 'A2' )
        switchB = net.addSwitch( 'B' )
        switchC = net.addSwitch( 'C' )
        switchD = net.addSwitch( 'D' )
        switchE = net.addSwitch( 'E' )
        switchF = net.addSwitch( 'F' )
        
        # Add OpenFlow controller
        c0 = net.addController(name='c0',controller=Controller)

        # Add links
        net.addLink( leftHost, switchA )
        net.addLink( switchA, switchA2 )
        net.addLink( switchA2, switchB )
        net.addLink( switchB, switchC )
        net.addLink( switchC, switchD )
        net.addLink( switchC, switchE )
        net.addLink( switchE, switchF )
        net.addLink( switchD, switchF )
        net.addLink( switchF, rightHost )

        # Start network
        info( '*** Starting controllers\n')
        c0.start()

        info( '*** Starting switches\n')
        net.get('A').start([c0])
        net.get('A2').start([c0])
        net.get('B').start([c0])
        net.get('C').start([c0])
        net.get('D').start([c0])
        net.get('E').start([c0])
        net.get('F').start([c0])

        info( '*** Post configure switches and hosts\n')
        CLI(net)
        


if __name__ == '__main__': 
    setLogLevel('info')  
    net = Lab1()
    net.start()
    
    print('\n\nHost connections:')
    dumpNodeConnections(net.hosts)
    
    print( '\n\nTesting network connectivity' )
    net.pingAll()
    net.stop()
    