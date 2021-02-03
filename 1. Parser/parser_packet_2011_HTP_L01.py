# -*- coding:utf-8 -*-

import socket
import dpkt

def extract(pcap):
    for ts,buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            tcp = ip.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            # http_req = dpkt.http.Request(tcp.data)
            # if http_req.uri.find('<script>') >=0:
            #     print http_req.uri
            if buf.find("<script>") != -1:
                print "[+] 출발지 : "+src+"도착지 : "+dst
                print buf
                # print buf[buf.find("<script>"):buf.find("</script>")+1],
        except:
            pass

def main():
    p = open('C:/2011_HTP_PreQual_PROB.pcap','rb')
    pcap = dpkt.pcap.Reader(p)
    extract(pcap)

if __name__=='__main__':
    main()
