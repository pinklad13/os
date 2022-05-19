import ipaddress

ip1 = ipaddress.IPv6Address('2a02:27b0:4a03:2bf0:c858:ff0c:af83:d7a7')
print(ip1.teredo)
ip2 = ipaddress.ip_address('2a02:27b0:4a03:2990:f0d9:a250:fd0a:40e3')

if ip1 == ip2:
    print('dpoe')

