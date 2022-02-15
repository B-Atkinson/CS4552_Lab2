# [4552] Code below is adapted from [<python3 packages]/ryu/app/simple_switch_12.py 
#
# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_2
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

# [4552] Add additional packet types 
from ryu.lib.packet import ipv4
from ryu.lib.packet import icmp


class SimpleSwitch12(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_2.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch12, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

        # [4552] start of sample custom code (block 1)
        self.icmp_count = 0
        self.icmpDict = {}
        # [4552] end of sample custom code (block 1)

    def add_flow(self, datapath, port, dst, src, actions):
        ofproto = datapath.ofproto

        match = datapath.ofproto_parser.OFPMatch(in_port=port,
                                                 eth_dst=dst,
                                                 eth_src=src)
        inst = [datapath.ofproto_parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS, actions)]
        
        mod = datapath.ofproto_parser.OFPFlowMod(
            datapath=datapath, cookie=0, cookie_mask=0, table_id=0,
            command=ofproto.OFPFC_ADD, idle_timeout=0, hard_timeout=1,
            priority=0, buffer_id=ofproto.OFP_NO_BUFFER,
            out_port=ofproto.OFPP_ANY,
            out_group=ofproto.OFPG_ANY,
            flags=0, match=match, instructions=inst)
        datapath.send_msg(mod)
        
    def blockFlow(self, datapath, port, dst, src):
        instruction = [datapath.ofproto_parser.OFPInstructionActions(datapath.ofproto.OFPIT_CLEAR_ACTIONS, [])]
        print(11)
        
        match = datapath.ofproto_parser.OFPMatch(in_port=port,eth_dst=dst,eth_src=src)
        print(12)
        msg = datapath.ofproto_parser.OFPFlowMod(self.datapath, table_id = 0, priority = 1,
                            command = datapath.ofproto.OFPFC_ADD,
                            match = match,
                            instructions = instruction
                            )
        print(13)
        datapath.send_msg(msg)
        print(14)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return

        # [4552] start of sample custom code (block 2)
        self.logger.info("ether_type: %s", eth.ethertype)
        if eth.ethertype == ether_types.ETH_TYPE_IP:
            # self.logger.info("received an IP packet")
            _ip = pkt.get_protocol(ipv4.ipv4)
            _icmp = pkt.get_protocol(icmp.icmp)
            if _ip:
                # self.logger.info("srcIP: %s, dstIP: %s", _ip.src, _ip.dst)
                pass
            if _icmp:
                try:
                    print(1)
                    self.icmp_count = self.icmp_count+1
                    print(2)
                    self.logger.info("received an ICMP packet, total: %s", self.icmp_count)
                    print(3)
                    # # self.logger.info("srcIP: %s, dstIP: %s", _ip.src, _ip.dst)
                    print(4)
                    
                    if (eth.src,eth.dst) in self.icmpDict:
                        print(5)
                        self.icmpDict[(eth.src,eth.dst)] += 1
                        print(6)
                    else:
                        print(7)
                        self.icmpDict[(eth.src,eth.dst)] = 1
                        print(8)
                    
                    if self.icmpDict[(eth.src,eth.dst)] > 3:
                        print(9)
                        #drop packets
                        self.logger.info("exceeded 10 flows, dropping packet.")
                        print(10)
                        self.blockFlow(datapath, in_port, eth.dst, eth.src)
                        print(15)
                        return
                except NameError:
                    self.logger.info("come here!!!")
                    self.icmp_count = 1

        # [4552] end of sample custom code (block 2)

        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            self.add_flow(datapath, in_port, dst, src, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,
            actions=actions, data=data)
        datapath.send_msg(out)
