#!/usr/bin/env python
#encoding=utf-8

from RenrenHandler import RenrenHandler
import networkx as nx
import random
import os, time, sys
# import pdb

class dataVisualizationHandler(object):
    """visualize friends relation"""
    def __init__(self):
        self.G = nx.Graph()
        self.min_node_size = 0.05
        self.max_node_size = 0.2

    def import_data(self, handler, friendsDict):
        self.handler = handler
        self.G = nx.Graph()  # Create a Graph object
        for uid1, uname1 in friendsDict.items():
            self.G.add_node(unicode(uname1))
            for uid2, uname2 in friendsDict.items():
                if uid2 == uid1:
                    continue
                if self.handler.getrelations(uid1, uid2):
                    self.G.add_edge(unicode(uname1), unicode(uname2))

        self.clear_nodes()
        self.degree = nx.degree(self.G)
        self.max_degree_value = max(self.degree.values())
        self.max_degree_value_floated = float(self.max_degree_value)

        return self.G
        
    def _clear_nodes(self):
        need_clear = False
        for n in self.G.nodes():
            if self.G.degree(n) < 2:
                self.G.remove_node(n)
                need_clear = True
                
        return need_clear

    def clear_nodes(self):
        while self._clear_nodes():
            pass
             
    def one_node_size(self, n):
        d = self.degree[n]
        d = d / self.max_degree_value_floated * self.max_node_size
        if d < self.min_node_size:
            d = self.min_node_size
        return d          
  
    def get_node_size(self, nodes):
        return [self.one_node_size(n) for n in nodes]
 
    def one_node_color(self, n):
        d = self.degree[n]
        if d > self.max_degree_value / 2:
            _range = [0.5, 0.8]
        else:
            _range = [0.8, 1.0]
            
        _make = lambda: random.uniform(*_range)
        _love = _make
        _ohyes = _make
        
        return (_make(), _love(), _ohyes())
   
    def get_node_color(self, nodes):
        return [self.one_node_color(n) for n in nodes]

    def save(self, it=55):
        if not os.path.exists("config/" + self.handler.userId + "/data/"):
                os.makedirs("config/" + self.handler.userId + "/data/")

        fd = "config/" + self.handler.userId + "/data/friendsRelation.dot"
        fp = "config/" + self.handler.userId + "/data/friendsRelation.png"
        # pdb.set_trace()
        try:
            nx.write_dot(self.G, fd)
        except Exception, e:
            print e
            time.sleep(5)
            sys.exit()

        import matplotlib.pyplot as plt
        
        pos = nx.spring_layout(self.G, iterations=it)
        
        nx.draw_networkx_edges(self.G, pos, alpha=0.1)
        
        nx.draw_networkx_nodes(
            self.G,
            pos,
            node_size = self.get_node_size(self.G.nodes()),
            node_color = self.get_node_color(self.G.nodes()),
            alpha = 0.8,
        )
        
        plt.axis('off')
        try:
            plt.savefig(fp, dpi=200)
            plt.clf()
        except Exception, e:
            print e
            time.sleep(5)
            sys.exit()


if __name__ == '__main__':
    username = "yourusername"
    password = "yourpassword"
    myRenren = RenrenHandler(username=username, password=password)
    myFriendsDict = myRenren.getFriendsDict(myRenren.userId)
    myDataVisualizationHandler = dataVisualizationHandler()
    g = myDataVisualizationHandler.import_data(myRenren, myFriendsDict)
    myDataVisualizationHandler.save()