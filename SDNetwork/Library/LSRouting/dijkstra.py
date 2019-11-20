#!/usr/bin/python
# -*- coding: utf-8 -*-

#

import math


def node_with_least_cost(unvisited_switches_dic):
	cost = float('inf')
	node = 0
	for i in (unvisited_switches_dic):
		if unvisited_switches_dic[i]<cost:
			cost = unvisited_switches_dic[i]
			node = i
	return node


def find_all_other_swtiches( link_and_weight):
	max = 1
	for i in range(len(link_and_weight)):
		if link_and_weight[i][0]>max:
			max = link_and_weight[i][0]
		if link_and_weight[i][1] >max:
			max = link_and_weight[i][1]
	return max


def remove_duplicate(link_and_weight):
	result = []
	for i in range(len(link_and_weight)):
		if link_and_weight[i][0]>link_and_weight[i][1]:
			tuple = (link_and_weight[i][1],link_and_weight[i][0],link_and_weight[i][2])
			if tuple not in result:
				result.append(tuple)
		else:
			result.append(link_and_weight[i])
	return result



def get_route(start_node,end_node,predecessors):
	route = []
	pred = predecessors[end_node]
	route.append(end_node)
	route.append( pred)
	while pred !=start_node:
		if pred in predecessors:
			pred = predecessors[pred]
			route.append(pred)
		else:
			print("The graph is disconnected from the start node to the end node, route not found!")
			return []
	route.reverse()
	return route


def get_routing_decision(start_node, link_and_weight, end_node = 0):#linl_and_weight: (node, node, weight)
	#do a remove duplicate here
	link_and_weight = remove_duplicate(link_and_weight)
	#make sure every node is connected


	visited_switches_dic = {}  # node:cost
	unvisited_switches_dic = {} #unvisited node
	switch_num = find_all_other_swtiches(link_and_weight) #total number of hosts
	predecessors= {}  # predecesor lists
	for i in range(switch_num):  #initialize all nodes except the start node to have a cost of inifinity
		if i+1!=start_node:
			unvisited_switches_dic[i+1] = float('inf')
		else:
			unvisited_switches_dic[i+1] =  0

	while len(visited_switches_dic)!=switch_num: #start to calculate least cost path to every node
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
	if end_node == 0:
		routes = []
		for i in range(switch_num):
			if i!= start_node:
				routes.append(get_route(start_node,i,predecessors))
		return routes
	else:
		return get_route(start_node,end_node,predecessors)
