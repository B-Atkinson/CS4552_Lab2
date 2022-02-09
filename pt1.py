#!/usr/bin/env python

"""
Create a network where different switches are connected to
different controllers, by creating a custom Switch() subclass.
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.topolib import TreeTopo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.util import dumpNodeConnections


class Lab1(Topo):
    '''The topology from Lab 1 with switches [A,A2,B,C,D,E,F], two hosts [H1, H2], and an SDN controller connected to switch D.'''
    def build(self):
        # Add hosts
        leftHost = self.addHost( 'h1' )
        rightHost = self.addHost( 'h2' )
        
        # Add switches
        switchA = self.addSwitch( 'A' )
        switchA2 = self.addSwitch( 'A2' )
        switchB = self.addSwitch( 'B' )
        switchC = self.addSwitch( 'C' )
        switchD = self.addSwitch( 'D' )
        switchE = self.addSwitch( 'E' )
        switchF = self.addSwitch( 'F' )
        
        # Add controller
        controller = self.addController('MAIN')

        # Add links
        self.addLink( leftHost, switchA )
        self.addLink( switchA, switchA2 )
        self.addLink( switchA2, switchB )
        self.addLink( switchB, switchC )
        self.addLink( switchC, switchD )
        self.addLink( switchC, switchE )
        self.addLink( switchE, switchF )
        self.addLink( switchD, switchF )
        self.addLink( switchF, rightHost )

if __name__ == '__main__': 
    setLogLevel('info')  
    topo = Lab1()
    net = Mininet(topo)
    net.start()
    
    print('\n\nHost connections:')
    dumpNodeConnections(net.hosts)
    
    print( '\n\nTesting network connectivity' )
    net.pingAll()
    net.stop()
    