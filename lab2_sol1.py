#!/usr/bin/python

################################################################
# 1. Must be run as root                                       #
# 2. Make executable with:                                     #
#    $ sudo chmod a+x lab2_new.py                              #
# 3. Start Ryu controller in seperate terminal window with:    #
#    $ ryu-manager ryu.app.simple_switch_13 ryu.app.ofctl_rest #
# 4. Run this script after controller is up:                   #
#    $ sudo ./lab2_new.py                                      #
################################################################

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def lab2Net():

    #net = Mininet( topo=None, build=False )

    net = Mininet(switch=OVSSwitch)

    info( '*** Adding controller\n' )
    c0 = net.addController('c0', port=6634)
    #c0 = net.addController('c0', controller=RemoteController)

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip='10.0.1.1' )
    h2 = net.addHost( 'h2', ip='10.0.2.1' )

    info( '*** Adding switches\n' )
    s1 = net.addSwitch( 's1', cls=OVSSwitch )
    s2 = net.addSwitch( 's2', cls=OVSSwitch )
    s3 = net.addSwitch( 's3', cls=OVSSwitch )
    s4 = net.addSwitch( 's4', cls=OVSSwitch )    
    s5 = net.addSwitch( 's5', cls=OVSSwitch )
    s6 = net.addSwitch( 's6', cls=OVSSwitch )

    info( '*** Creating links\n' )
    #net.addLink( c0, s5 )
    net.addLink( h1, s1 )
    net.addLink( s1, s2 )
    net.addLink( s2, s3 )
    net.addLink( s3, s4 )
    net.addLink( s3, s5 )
    net.addLink( s4, s6 )
    net.addLink( s5, s6 )
    net.addLink( s6, h2 )

    info( '*** Starting controller at s4\n')
    s4.start([c0])

    info( '*** Starting network\n')
    net.start()

    info('*** Enable spanning tree\n')                   
    s1.cmd('ovs-vsctl set bridge s1 stp-enable=true')
    s2.cmd('ovs-vsctl set bridge s2 stp-enable=true')
    s3.cmd('ovs-vsctl set bridge s3 stp-enable=true')
    s4.cmd('ovs-vsctl set bridge s4 stp-enable=true')
    s5.cmd('ovs-vsctl set bridge s5 stp-enable=true')
    s6.cmd('ovs-vsctl set bridge s6 stp-enable=true')

    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    lab2Net()
