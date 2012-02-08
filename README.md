Description
===========
OpenDomi is the open source clone of [Domi](http://www.domain.hu/domain/regcheck/), the domain checking utility made by [Council of Hungarian Internet Providers](http://www.iszt.hu/iszt/) (ISZT), the .hu ccTLD registry.

Output of original Domi:

	M-GREET -I- [iszt.hu] Domi version 20120103
	M-STAR -I- [iszt.hu] NS parameter not given, getting it from DNS
	M-PNAM -I- [iszt.hu] NS name: ns.iszt.hu
	M-PADD -I- [iszt.hu] NS addr: 193.239.149.116
	M-PGET -I- [iszt.hu] getting domain from NS 193.239.149.116 ...
	M-ROK -I- [iszt.hu] SOA parameters comply with RIPE
	M-NS -I- [iszt.hu] A records for DNS servers:
	addr of NS ns.iszt.hu.: 193.239.149.116
	addr of NS ns-s.nic.hu.: 193.225.195.195
	M-SOA -I- [iszt.hu] A record for SOA mail host nic.hu:
	addr of MX deneb.iszt.hu.: 193.239.149.6
	M-MX -I- [iszt.hu] A records for MX records:
	addr of MX deneb.iszt.hu.: 193.239.149.6
	M-TRNO -I- [iszt.hu] skipping traceroute, servers on diff nets 193.239.149.116 193.225.195.195
	M-NSC -I- [iszt.hu] checking NS records ...
	M-SGET -I- [iszt.hu] getting data from 193.225.195.195 ns-s.nic.hu ...
	M-PMAI -I- [iszt.hu] checking postmaster e-mail at deneb.iszt.hu, 193.239.149.6 ...
	M-VOUT -I- [iszt.hu] address verification: 2.1.5 Ok
	M-MXOK -I- [iszt.hu] MX server okay
	M-SMAI -I- [iszt.hu] checking SOA mail hostmaster@nic.hu at 193.239.149.6
	M-VOUT -I- [iszt.hu] address verification: 2.1.5 Ok
	M-MXOK -I- [iszt.hu] MX server okay
	M-OK -S- [iszt.hu] All's well............ that ends well................. 

Motivation
==========
I have started this project this because ISZT refused to open the source of Domi.
