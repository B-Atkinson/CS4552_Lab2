#!/usr/bin/env python

"""
Create a network where different switches are connected to
different controllers, by creating a custom Switch() subclass.
"""
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.util import dumpNodeConnections


def Lab1():
    net = Mininet(switch=OVSSwitch)
    
    # Add hosts
    info( '*** Adding hosts')
    leftHost = net.addHost( 'h1', ip='10.0.2.1' )
    rightHost = net.addHost( 'h2', ip='10.0.2.2' )
    
    # Add switches
    info( '*** Adding switches')
    switchA = net.addSwitch( 's1', cls=OVSSwitch )
    switchA2 = net.addSwitch( 's2', cls=OVSSwitch )
    switchB = net.addSwitch( 's3', cls=OVSSwitch )
    switchC = net.addSwitch( 's4', cls=OVSSwitch )
    switchD = net.addSwitch( 's5', cls=OVSSwitch )
    switchE = net.addSwitch( 's6', cls=OVSSwitch )
    switchF = net.addSwitch( 's7', cls=OVSSwitch )
    
    # Add OpenFlow controller
    info( '*** Adding controllers')
    c0 = net.addController(name='c0',port=6684)
    
    # Add links
    info( '*** Adding links')
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
    info( '*** Starting controllers')
    switchD.start([c0])
    net.start()
    
    
    info( '*** Starting switches\n')
    switchA.cmd('ovs-vsct1 set bridge s1 stp-enable=true')
    switchA2.cmd('ovs-vsct1 set bridge s2 stp-enable=true')
    switchB.cmd('ovs-vsct1 set bridge s3 stp-enable=true')
    switchC.cmd('ovs-vsct1 set bridge s4 stp-enable=true')
    switchD.cmd('ovs-vsct1 set bridge s5 stp-enable=true')
    switchE.cmd('ovs-vsct1 set bridge s6 stp-enable=true')
    switchF.cmd('ovs-vsct1 set bridge s7 stp-enable=true')

    info('***Running network***')
    CLI(net)
    
    info('***Stopping network')
    net.stop()
    
if __name__ == '__main__': 
    setLogLevel('info') 
    Lab1()
    