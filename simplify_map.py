import networkx as nx
import matplotlib.pyplot as plt

# ----------------------create by Rao Wenjun in 2021----------------------
# 节点属性中node_type为0即表示该节点为资源，若为1则表示该节点为进程.
# 图中边的权值即为申请/分配的资源数
#
#
#
#
def add_a_edge(start, end, w):
    G.add_edge(start, end, weight = w)

def add_a_node(name, type, s = -1):
    G.add_node(name, node_type = type, source = s, safe = 0)

def jdg(node_in):                                   # 传入一个节点，若其申请的资源都能得到满足，则返回True.
    if G.nodes[node_in]['node_type'] == 0:          #判断传入节点是否为进程.
        return False
    successors = (list(G.successors(node_in)))
    for i in successors:
        if G.edges[(node_in, i)]['weight'] > G.nodes[i]['source']:
            return False
    G.nodes[node_in]['safe'] = 1
    return True

def distri():                                       # 将图中资源都减去已分配的.
    for i in list(G.nodes):
        if G.nodes[i]['node_type'] == 0:
            successors = (list(G.successors(i)))
            for j in successors:
                w = G.edges[(i, j)]['weight']
                G.nodes[i]['source'] -= w

def del_node(node_in):                              # 孤立一个节点，即删除与其相连的所有边.
    successors = (list(G.successors(node_in)))
    for i in successors:
         G.remove_edge(node_in, i)
    predecessors = (list(G.predecessors(node_in)))
    for j in predecessors:
         G.remove_edge(j, node_in)

def Souce_Return(node_in):                        #释放一个节点所占有的资源.
    predecessors = (list(G.predecessors(node_in)))
    for i in predecessors:
        w = G.edges[(i, node_in)]['weight']
        G.nodes[i]['source'] += w

def simplify(times):                              #化简资源分配图.
    distri()
    for a in range(times):
        for key in G.nodes:
            if (jdg(key)):
                Souce_Return(key)
                del_node(key)
                break

def Safe():                                     #判断系统是否安全，即判断图中是否还有边.
    if G.size() == 0:
        print("系统安全，不发生死锁。")
    else:
        print("系统不安全，将发生死锁，死锁进程有:")
        for key in G.nodes:
            if G.nodes[key]['safe'] == 0 and G.nodes[key]['node_type'] == 1:
                print(key)

def print_map():                                #画图,围绕圆心分布.
    pos = nx.circular_layout(G, scale=5)
    nx.draw(G, with_labels=True, pos=pos)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()





G = nx.DiGraph()
Source_num = int(input("请输入待被分配的资源数:"))
Processes_num =int(input("请输入等待分配的进程数:"))
for i in range(Source_num + 1):
    if i == 0:
        continue
    print("请输入R%d的资源总数:" % (i))
    s = int(input())
    add_a_node('R' + str(i), 0, s)

for i in range(Processes_num + 1):
    if i == 0:
        continue
    for j in range(Source_num + 1):
        if j == 0:
            continue
        print("请输入P%d进程分配到的R%d资源数:" % (i, j))
        s = int(input())
        add_a_node('P' + str(i), 1)
        if s == 0:
            continue
        add_a_edge('R' + str(j), 'P' + str(i), s)
    for k in range(Source_num + 1):
        if k == 0:
            continue
        print("请输入P%d进程申请的R%d资源数:" % (i, k))
        s = int(input())
        if s == 0:
            continue
        add_a_edge('P' + str(i), 'R' + str(k), s)

print_map()
simplify(Processes_num)                     #循环执行的最多次数和图中进程数一致.
Safe()
print_map()