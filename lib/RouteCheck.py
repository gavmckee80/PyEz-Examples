import xmltodict
import hashlib
from lxml import etree
from jnpr.junos.op.routes import RouteTable, RouteSummaryTable
from sets import Set

class RouteTableCheck():

	def __init__(self, pre_xml, post_xml):
		# pre and post_xml are the XML responses returned from the device
		self.pre_xml = pre_xml
		self.post_xml = post_xml

	def get_pre_dict(self):
		return self.pre_xml

	def get_post_dict(self):
		return self.post_xml


# the following function checks the pre and post routing tables for routes that
# have gone missing from the pre to the post snapshot.  This function prints the 
# details of any route that has gone missing from the table

	def check_missing(self):
		pre_routes = self.rt_to_dict(self.pre_xml)
		post_routes = self.rt_to_dict(self.post_xml)

		s1 = Set(pre_routes.keys())
		s2 = Set(post_routes.keys())

		for x in s1 - s2:
			print pre_routes[x]['table-name'],pre_routes[x]['rt-destination'],pre_routes[x]['protocol-name']

	def check_added(self):
		pre_routes = self.rt_to_dict(self.pre_xml)
		post_routes = self.rt_to_dict(self.post_xml)

		s1 = Set(pre_routes.keys())
		s2 = Set(post_routes.keys())

		for x in s2 - s1:
			print post_routes[x]['table-name'],post_routes[x]['rt-destination'],post_routes[x]['protocol-name']


	def rt_to_dict(self, xml):
		pre_dict = xmltodict.parse(etree.tostring(xml))

		route_dict = {}

		for rib in pre_dict['route-information']['route-table']:
			for prefix in rib['rt']:
				try:
					route_dict.update({hashlib.sha224(rib['table-name']+prefix['rt-destination']).hexdigest():
						{'table-name':rib["table-name"], 
						"rt-destination":prefix["rt-destination"],
						"protocol-name":prefix['rt-entry']["protocol-name"],
						"as-path":prefix["rt-entry"]["as-path"],
						"age":prefix["rt-entry"]['age']['@seconds'],
						"nh": prefix["rt-entry"]["nh"]
						}})
				except (TypeError, KeyError):
					try:
						route_dict.update({hashlib.sha224(rib['table-name']+prefix['rt-destination']).hexdigest():
							{'table-name':rib["table-name"], 
							"rt-destination":prefix["rt-destination"],
							"protocol-name":prefix['rt-entry']["protocol-name"],
							"age":prefix["rt-entry"]['age']['@seconds'],
							"nh": prefix["rt-entry"]["nh"]
							}})
					except (TypeError, KeyError):
						try:
							route_dict.update({hashlib.sha224(rib['table-name']+prefix['rt-destination']).hexdigest():
								{'table-name':rib["table-name"], 
								"rt-destination":prefix["rt-destination"],
								"protocol-name":prefix['rt-entry']["protocol-name"],
								"age":prefix["rt-entry"]['age']['@seconds'],
								"nh": prefix["rt-entry"]["nh"]
								}})
						except(TypeError, KeyError):
							pass
						pass
					pass

		return route_dict

pre_rt = RouteTable(path='/home/gmckee/Documents/snapshots/R1-pre-routetable.xml').get()
post_rt = RouteTable(path='/home/gmckee/Documents/snapshots/R1-post-routetable.xml').get()

check = RouteTableCheck(pre_rt.xml,post_rt.xml)

print "INFO: Checking if routes are missing post change...\n", check.check_missing()



