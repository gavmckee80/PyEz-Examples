# Writing some code to allow us to modify an xml reponse to unit test the code
#just some ideas

# to remove an entire route table from an XML file the following code looks good
for x in rt.xml.xpath('route-table'):
  for y in x.findall('table-name'):
    if y.text != 'L3VPN01.inet.0':
      x.getparent().remove(x)


# Algorithm to randomly select routes for deletion from the routing table
# depending on the number of routes that we delete we will have to update
# the count fields to reflect the number of routes that are removed
for x in rt.xml.xpath('route-table'):
  tblname = [tn.text for tn in x.findall('table-name')]
  for y in x.findall('rt'):
    for z in y.findall('rt-destination'):
      if z.text != '219.0.0.0/9':             #here we are testing using a randomly choosen prefix
        y.getparent().remove(y)
        print tblname[0], z.text


import random

for table in rt.xml.xpath('route-table'):
  tblname = [tn.text for tn in table.findall('table-name')]
  prefix_list = []
  for route in table.findall('rt'):
    for dest in route.findall('rt-destination'):
      prefix_list.append(dest.text)
      
  # generate a random int based on the total number of prefixes in the list
  # this will be the total number of route removed from the table
  x = random.randint(1,len(prefix_list))  

for table in pre_xml.xml.xpath('route-table'):
  if table.xpath('table-name')[0].text == post_xml.xml.xpath('route-table/table-name')[0].text:
    print  table.xpath('table-name')[0].text, [x.text for x in table.xpath('rt/rt-destination')] 
