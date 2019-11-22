import math


def node_with_least_cost(unvisited_switches_dic):
	cost = float('inf')
	node = ""
	for i in (unvisited_switches_dic):
		if unvisited_switches_dic[i]<cost:
			cost = unvisited_switches_dic[i]
			node = i
#	print("this cost", cost)
	return node


def find_all_other_swtiches( link_and_weight):
	result =[]
	for i in link_and_weight:
		if i[0] not in result:
			result.append(i[0])
		if i[1] not in result:
			result.append(i[1])
	return result


def remove_duplicate(link_and_weight):#('switch1', 'switch2, weight)
	result = []
	for i in range(len(link_and_weight)):
		j = 0
		while 1:
			if j < len(link_and_weight[i][0]) and j< len(link_and_weight[i][1]):
				if link_and_weight[i][0][j]>link_and_weight[i][1][j]:
					if(link_and_weight[i] not in result):
						result.append(link_and_weight[i])
					break
				elif link_and_weight[i][0][j]<link_and_weight[i][1][j]:
					tuple = (link_and_weight[i][1],link_and_weight[i][0],link_and_weight[i][2])
					if tuple not in result:
						result.append(tuple)
					break
				else:
					j = j + 1
			else:# s1 is longer in length
				if len(link_and_weight[i][0]) > len(link_and_weight[i][1]):
					if (link_and_weight[i] not in result):
						result.append(link_and_weight[i])
					break
				else: #s2 is longer in length
					tuple = (link_and_weight[i][1], link_and_weight[i][0], link_and_weight[i][2])
					if tuple not in result:
						result.append(tuple)
					break
	return result






def get_route(start_node,end_node,predecessors):
	temp = []
	if end_node not in predecessors:
#		print("node not reachable")
		return (start_node,[])
	pred = predecessors[end_node]

	temp.append(end_node)
	temp.append(pred)
	while pred !=start_node:
			pred = predecessors[pred]
			temp.append(pred)
	temp.reverse()
	route = (end_node,temp)
	return route

def convert_to_string(link_and_weight):
	result = []
	for i in link_and_weight:
		tuple = (str(i[0]),str(i[1]), i[2])
		result.append(tuple)
	return result


def get_routing_decision(start_node, link_and_weight, end_node = ""):#linl_and_weight: (node, node, weight)
	#do a remove duplicate here
	link_and_weight = remove_duplicate(link_and_weight)
	link_and_weight = convert_to_string(link_and_weight)
	#print(link_and_weight)

	visited_switches_dic = {}  # node:cost
	unvisited_switches_dic = {} #unvisited node
	all_switches = find_all_other_swtiches(link_and_weight) #total number of hosts
	predecessors= {}  # predecesor dics
	for i in all_switches:  #initialize all nodes except the start node to have a cost of inifinity
		if i!=start_node:
			unvisited_switches_dic[i] = float('inf')
		else:
			unvisited_switches_dic[i] = 0

	while len(visited_switches_dic)!=len(all_switches): #start to calculate least cost path to every node
		current_node = node_with_least_cost(unvisited_switches_dic) #get the least node with least cost
		visited_switches_dic[current_node] = unvisited_switches_dic[current_node] #set this node to be visited
		unvisited_switches_dic.pop(current_node) # and remove this node from unvisited
		disconnected_graph = True
		for i in range(len(link_and_weight)):
			# find all links from current_node to adjacent nodes
			if link_and_weight[i][0] == current_node and link_and_weight[i][1] in unvisited_switches_dic:
				if visited_switches_dic[current_node] + link_and_weight[i][2] < unvisited_switches_dic[link_and_weight[i][1]]:
					predecessors[link_and_weight[i][1]] = current_node
					unvisited_switches_dic[link_and_weight[i][1]] = visited_switches_dic[current_node] + link_and_weight[i][2]
					disconnected_graph = False
			if link_and_weight[i][1] == current_node and link_and_weight[i][0] in unvisited_switches_dic:
				if visited_switches_dic[current_node] + link_and_weight[i][2] < unvisited_switches_dic[link_and_weight[i][0]]:
					predecessors[link_and_weight[i][0]] = current_node
					unvisited_switches_dic[link_and_weight[i][0]] = visited_switches_dic[current_node] + link_and_weight[i][2]
					disconnected_graph = False
		if disconnected_graph == True:
			break
	if end_node == "":
		routes = []
		for i in all_switches:
			if i!= start_node:
				routes.append(get_route(start_node,i,predecessors))
		return routes
	else:
		return get_route(start_node,end_node,predecessors)








