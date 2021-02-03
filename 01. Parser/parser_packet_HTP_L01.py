# -*- coding:utf-8 -*-

import socket
import dpkt
import datetime

def mac_addr(address):
    return ':'.join('%02x' % ord(mac) for mac in address)

def extract(pcap):
    for timestamp,data in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(data)
            ip = eth.data
            tcp = ip.data
            src,dst = socket.inet_ntoa(ip.src),socket.inet_ntoa(ip.dst)
            if tcp.dport==23 or tcp.sport==23 and len(tcp.data)>=0:
                # request = dpkt.http.Request(tcp.data)            
                print "[+] Timestamp : ",datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                print "[+] MAC Address  : ",mac_addr(eth.src), ' --> ', mac_addr(eth.dst)
                print "[+] IP Address   : ",src+" --> "+dst
                print "[+] Data         : ",data
                print "\n",
        except:
            pass

def main():
    p = open('C:/2013_Hack_The_Packet_Online_PreQUAL_PROB.pcap','rb')
    pcap = dpkt.pcap.Reader(p)
    extract(pcap)

if __name__=='__main__':
    main()
