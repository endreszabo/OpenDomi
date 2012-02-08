#!/usr/bin/env python2

# endre szabo, GPLv2, 2012, WIP

from sys import argv
from random import choice

import dns

if len(argv)>1:
    domain=argv[1]
else:
    domain='end.re'

print "M-GREET -I- [%s] OpenDomi version 20120208" % domain

import dns.query
import dns.resolver
from dns.exception import DNSException

default_soa={
    'refresh' : 86400,        # 24 hours
    'retry'   : 7200,         # 2 hours
    'expire'  : 2419200,      # 4 weeks
    'ttl'     : 3600          # 1 hour
}

cache=[]

def query(domain, rdatatype=dns.rdatatype.A, ns=None):
    if not ns:
        default = dns.resolver.get_default_resolver()
        ns = choice(default.nameservers)
    query = dns.message.make_query(domain, rdatatype)
    response = dns.query.udp(query, ns[1])
    return query

def dump_response(response):
    print dir(response)
    print "\n;; Response for Question\n"
    for rrset in response.question:
        print rrset.to_text()
    print "\n;; Response Authority\n"
    for rrset in response.authority:
        print rrset.to_text()
    print "\n;; Response Answer\n"
    for rrset in response.answer:
        print rrset.to_text()
    print "\n;; Response Additional\n"
    for rrset in response.additional:
        print rrset.to_text()

def check_soa(ns):
    query = dns.message.make_query(domain, dns.rdatatype.SOA)
    response = dns.query.udp(query, ns[1])

    rcode = response.rcode()
    if rcode != dns.rcode.NOERROR:
        log('PRIF','E','Cannot get domain data: %s (%s %s)' % (dns.rcode.to_text(rcode,ns[1],ns[0])))

    if (len(response.answer)!=1):
        log('PRIF','E','Got %d SOA records' % len(response.answer))
    else:
        log('PRIF','I','Got %d SOA record' % len(response.answer))
    soa=response.answer[0].items[0].to_text()
    print "Got soa value: '%s'" % soa
    soa_fields=soa.split(' ')
    if len(soa_fields) != 7:
        log('PRIF','E','Wrong number of SOA fields: %d', len(soa_fields))
    soa_error=[]
    if soa_fields[3] * 20 > default_soa['refresh'] or soa_fields[3] / 20 < default_soa['refresh']:
        soa_error+=['refresh: %s' % soa_fields[3]]
    if soa_fields[3] * 20 > default_soa['retry'] or soa_fields[3] / 20 < default_soa['retry']:
        soa_error+=['retry: %s' % soa_fields[3]]
    if soa_fields[3] * 20 > default_soa['expire'] or soa_fields[3] / 20 < default_soa['expire']:
        soa_error+=['expire: %s' % soa_fields[3]]
    if soa_fields[3] * 20 > default_soa['ttl'] or soa_fields[3] / 20 < default_soa['ttl']:
        soa_error+=['ttl: %s' % soa_fields[3]]
    if soa_error:
        log('RERR','W',"SOA parameters (%s) don't comply with RIPE" % ', '.join(soa_error))

def query_authoritative_ns (domain, log=lambda msg: None):

    default = dns.resolver.get_default_resolver()
    ns = choice(default.nameservers)

    n = domain.split('.')+['.']

    for i in xrange(len(n), 0, -1):
        if i==len(n):
            sub = '.'.join(n[i-1:])
        else:
            sub = '.'.join(n[i-1:-1])
        print sub,i

        log('FQAN','D0','Looking up %s on %s' % (sub, ns))
        query = dns.message.make_query(sub, dns.rdatatype.NS)
        response = dns.query.udp(query, ns)

        rcode = response.rcode()
        if rcode != dns.rcode.NOERROR:
            if rcode == dns.rcode.NXDOMAIN:
                log('PRIF','E',"Cannot get domain data (%s %s)")
            else:
                raise Exception('Error %s' % (dns.rcode.to_text(rcode)))

        #dump_response(response)
        if len(response.authority) > 0:
            rrsets = response.authority
        elif len(response.additional) > 0:
            rrsets = [response.additional]
        else:
            rrsets = response.answer
        ns=[]

        for rrset in rrsets:
            for rr in rrset:
                if rr.rdtype == dns.rdatatype.SOA:
                    log('FQAN','D1','Same server is authoritative for %s' % (sub))
                    pass
                elif rr.rdtype == dns.rdatatype.A:
                    ns += [rr.items[0].address]
                    log('FQAN','D2','IPv4 ipv4 record for %s: %s' % (rr.name, rr.items[0].address))
                #elif rr.rdtype == dns.rdatatype.AAAA:
                #    ns += [rr.items[0].address]
                #    log('FQAN','D','IPv6 ipv6 record for %s: %s' % (rr.name, rr.items[0].address))
                elif rr.rdtype == dns.rdatatype.NS:
                    authority = rr.target
                    ns += [default.query(authority).rrset[0].to_text()]
                    log('FQAN','D3','%s [%s] is authoritative for %s; ttl %i' % (authority, default.query(authority).rrset[0].to_text(), sub, rrset.ttl))
                    result = [rr.to_text(), default.query(authority).rrset[0].to_text()] #choice(rrset) #pick a random NS
                else:
                    log('FQAN','D4',"Ignoring %s" % (rr))
                    pass
        print "Picking random ns from list:", ', '.join(ns)
        ns = choice(ns)
        print "Picked %s" % ns

    return result

import sys

def log (code, severity, msg):
    sys.stderr.write(u'M-' + code + ' -' + severity + '- [' + domain + '] ' + msg + u'\n')

if len(argv)<2:
    log('STAR','I','NS parameter not given, getting it from DNS')
    ns= query_authoritative_ns (domain, log)
    log('PNAM','I',"NS name: %s" % ns[0])
    log('PADD','I',"NS addr: %s" % ns[1])
else:
    ns=argv[2]

log('PGET','I','getting domain from NS %s' % ns[1])

check_soa(ns)


