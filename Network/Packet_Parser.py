import socket
import dpkt

path = "C:/test.pcap"

def display():
    print "\t[-] TYPE : {}".format(protocol)
    print "\t[-] MAC : {} ---> {}".format(smac, dmac)
    print "\t[-] LEN : {}".format(int(total_len, 16))
    print "\t[-] TTL : {}".format(int(ttl, 16))
    print "\t[-] IP : {} ---> {}".format(sip, dip)
    print "\t[-] PORT : {} ---> {}".format(int(sport, 16), int(dport, 16))

with open(path,'rb') as p:
    magic = p.read(4).encode('hex')
    flag = (False, True)[magic == "d4c3b2a1"]
    p.seek(36,1)
    dmac = p.read(6).encode('hex')
    smac = p.read(6).encode('hex')
    type = p.read(2).encode('hex')
    type = ("IPv6","IPv4")[type=="0800"]


    if flag==True:
        print "[+] Start parsing : {}".format(path)

        if type=="IPv4":
            p.seek(2,1) ; total_len = p.read(2).encode('hex')
            p.seek(4,1) ; ttl = p.read(1).encode('hex')
            protocol = p.read(1).encode('hex')
            protocol = ("","TCP")[protocol=="06"]

            p.seek(2,1)
            sip = p.read(4).encode('hex')
            dip = p.read(4).encode('hex')
            sport = p.read(2).encode('hex')
            dport = p.read(2).encode('hex')

            ip_divide = range(0, 8, 2) ; mac_divide = range(0,12,2)
            sip = '.'.join([str(int(sip[a:a+2],16)) for a in ip_divide])
            dip = '.'.join([str(int(dip[b:b+2],16)) for b in ip_divide])
            smac = ':'.join([str((smac[c:c+2])) for c in mac_divide]).upper()
            dmac = ':'.join([str((dmac[d:d+2])) for d in mac_divide]).upper()

            display()

        elif type=="IPv6":
            print("\t[-] It is IPv6 Packet")

    elif flag==False:
        print "[-] {} is not pcap file".format(path)
