for pre_rib in pre_rt.xml.xpath('route-table/table-name'):
  for post_rib in post_rt.xml.xpath('route-table/table-name'):
    if pre_rib.text == post_rib.text:
      for pre_prefix in pre_rib.xpath('../rt/rt-destination'):
        for post_prefix in post_rib.xpath('../rt/rt-destination'):
          if pre_prefix.text == post_prefix.text:
            for pre_protocol in pre_rib.xpath('../rt/rt-entry/protocol-name'):
              for post_protocol in post_rib.xpath('../rt/rt-entry/protocol-name'):
                if (pre_protocol.text == 'BGP') and (post_protocol.text == 'BGP') and (pre_protocol.text == post_protocol.text):
                  print "PRE: ", pre_rib.text, pre_prefix.text, pre_protocol.text
                  print "POST: ", post_rib.text, post_prefix.text, post_protocol.text
            
rt/rt-entry/protocol-name

dict1 = {}

for pre_rib in pre_rt.xml.xpath('route-table/table-name'):
  for prefix in pre_rib.xpath('../rt/rt-destination'):
    for protocol in pre_rib.xpath('../rt/rt-entry/protocol-name'):
      if protocol.text == 'BGP':
        dict1.update({hashlib.sha256(prefix.text+pre_rib.text+protocol.text).hexdigest():{'table-name': pre_rib.text,'protocol-name':protocol.text,'as-path': [protocol.xpath('../as-path')[0].text]}})

print dict1
