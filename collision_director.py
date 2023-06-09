from block_mechanism import BlockMechanism
from leaf_blocks import CoreBlock
from block import Block
import numpy as np

class CollisionDirector():
    # TODO: do force to block_mecha1 and block_mecha2 
    def is_collide(self,block_mechanism_1:BlockMechanism, block_mechanism_2:BlockMechanism):
        for _, block1 in block_mechanism_1.get_blocks().items():
            for _, block2 in block_mechanism_2.get_blocks().items():
                if self.is_block_collide(block1, block2):
                    # print(block1, block2)
                    return True
        return False
                
    def is_block_collide(self, block1:Block, block2:Block) -> bool:
        # block2's node in block1
        for node_index in range(len(block2.get_nodes())):
            if self.is_node_in_block(block2.get_nodes()[node_index], block1):
                node = tuple(block2.get_nodes()[node_index])
                impact_line = [block2.get_previous_nodes()[node_index], tuple(block2.get_nodes()[node_index])]
                impact_line[0] = ((impact_line[0][0]-impact_line[1][0])*100+impact_line[1][0], (impact_line[0][1]-impact_line[1][1])*100+impact_line[1][1])
                for line in block1.get_lines():
                    if self._detect_crossover(line, impact_line):
                        print(node, self._normal_vector_for_impactor(impact_line, line))
                return True
        return False

    def is_node_in_block(self, node:tuple, block:Block) -> bool:
        '''
        if there is a node which is in the block, return the node
        '''
        nodes = block.get_nodes()
        if not ((nodes[0][0]-nodes[1][0]) == 0 or (nodes[2][0]-nodes[1][0]) == 0):
            ma = (nodes[0][1]-nodes[1][1])/(nodes[0][0]-nodes[1][0])
            b1 = nodes[1][1]-ma*nodes[1][0]
            b2 = nodes[2][1]-ma*nodes[2][0]
            bt = node[1]-ma*node[0]
            if not ((b2 >= bt and bt >= b1) or (b1 >= bt and bt >= b2)):
                return False
            
            mb = ((nodes[2][1]-nodes[1][1])/(nodes[2][0]-nodes[1][0]))
            b1 = nodes[1][1]-mb*nodes[1][0]
            b0 = nodes[0][1]-mb*nodes[0][0]
            btt = node[1]-mb*node[0]
            if not ((b1 >= btt and btt >= b0) or (b0 >= btt and btt >= b1)):
                return False
        
            return True
        else:
            # x coor
            if not ((nodes[1][0] >= node[0] and node[0] >= nodes[3][0]) or (nodes[3][0] >= node[0] and node[0] >= nodes[1][0])):
                return False
            
            # y coor
            if not ((nodes[1][1] >= node[1] and node[1] >= nodes[3][1]) or (nodes[3][1] >= node[1] and node[1] >= nodes[1][1])):
                return False
            
            return True
        
    def _normal_vector_for_impactor(self, impact_line, hit_line) -> np.ndarray:
        '''
        hit line been hit by node
        '''
        v1 = np.array([impact_line[1][0]-impact_line[0][0], impact_line[1][1]-impact_line[1][0]]).transpose()
        v2 = np.array([hit_line[1][0]-hit_line[0][0], hit_line[1][1]-hit_line[1][0]]).transpose()
        vn = v1 - (np.dot(v1, v2)/np.dot(v2, v2))*v2
        vn = -1*(vn/np.linalg.norm(vn))
        return vn
              
    def _detect_crossover(self, line1:tuple, line2:tuple) -> bool:
        '''
        line is made of two points ((x1, y1), (x2, y2))
        '''
        # ax + by = c
        # y - y0 = m(x - x0)
        # (y-y0) = mx - mx0
        # y-y0-mx = -mx0
        # y - mx = y0 - mx0
        # print(f"line1:{line1}")
        # print(f"line2:{line2}")
        line2_points_for_line1 = False
        try:
            m1 = (line1[1][1]-line1[0][1])/(line1[1][0]-line1[0][0])
            line1_equation = lambda x, y: y - (line1[1][1]-line1[0][1])/(line1[1][0]-line1[0][0])*x
            answer_if_on_line1 = line1[0][1]-m1*line1[0][0]
            
            if not ((line1_equation(line2[0][0], line2[0][1]) > answer_if_on_line1 and line1_equation(line2[1][0], line2[1][1]) > answer_if_on_line1) or\
                (line1_equation(line2[0][0], line2[0][1]) < answer_if_on_line1 and line1_equation(line2[1][0], line2[1][1]) < answer_if_on_line1)):
                # print("CROSSOVER")
                line2_points_for_line1 = True
        except ZeroDivisionError:
            x = line1[0][0]
            if not ((line2[0][0] > x and line2[1][0] > x) or (line2[0][0] < x and line2[1][0] < x)):
                # print("CROSSOVER")
                line2_points_for_line1 = True
                
        line1_points_for_line2 = False
        try:
            m2 = (line2[1][1]-line2[0][1])/(line2[1][0]-line2[0][0])
            line2_equation = lambda x, y: y - (line2[1][1]-line2[0][1])/(line2[1][0]-line2[0][0])*x
            answer_if_on_line2 = line2[0][1]-m2*line2[0][0]
            
            if not ((line2_equation(line1[0][0], line1[0][1]) > answer_if_on_line2 and line2_equation(line1[1][0], line1[1][1]) > answer_if_on_line2) or\
                (line2_equation(line1[0][0], line1[0][1]) < answer_if_on_line2 and line2_equation(line1[1][0], line1[1][1]) < answer_if_on_line2)):
                # print("CROSSOVER")
                line1_points_for_line2 = True
        except ZeroDivisionError:
            x = line2[0][0]
            if not ((line1[0][0] > x and line1[1][0] > x) or (line1[0][0] < x and line1[1][0] < x)):
                # print("CROSSOVER")
                line1_points_for_line2 = True
                
        return line2_points_for_line1 and line1_points_for_line2
    
if __name__ == "__main__":
    director = CollisionDirector()
    test_tuples = ([0.3831967323152515, 0.736525937068662], [-0.08351638136233075, -0.14788283127399723]), ((-0.055232945952253275, -0.12299851137811744), (-0.0547465700639338, -0.12021249461175632))
    print(director._detect_crossover(test_tuples[0], test_tuples[1]))