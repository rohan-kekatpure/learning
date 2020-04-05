import bpy
import bpy_aarwild_280 as ba
import os
import json 
from collections import defaultdict

class Part:
    def __init__(self, data):
        self.part_data = data
        self.instance_num = 0

    def __getitem__(self, key):
        return self.part_data[key]

    def update(self):
        """
        Updates ids of socks and plugs to account for 
        prev instances in a blender scene. E.g. if
        two legs with <id> are already present in the 
        blender scene, then the default socket name of
        `<id>_sock_0.000` will be renamed to
        `<id>_sock_0.002`. Similarly for plugs.
        """        
        if self.instance_num == 0:
            return
    
        data = self.part_data 

        for port_type in ['sockets', 'plugs']:
            for port_subtype, port_data in data[port_type].items():                
                for i in range(port_data['count']):
                    vals = {
                        'id': data['id'], 
                        'port_subtype': port_subtype, 
                        'count': i, 
                        'inst': '{:03d}'.format(self.instance_num)
                    }
                    new_name = '{id}_{port_subtype}_{count}.{inst}'.format(**vals)
                    data[port_type][port_subtype]['names'][i] = new_name 
                    

class Partlib:
    def __init__(self, path):
        self.path = path

    def load(self, part_id):
        part_dir = os.path.join(self.path, part_id)

        # Load part mesh
        mesh_path = os.path.join(part_dir, 'mesh.dae')
        ba.load_collada_dae(mesh_path)

        # Load part metadata
        md_path = os.path.join(part_dir, 'mesh.json')
        with open(md_path) as f:
            data = json.load(f)

        return Part(data)


class Builder:
    """
    Builds the item given an adjacency list
    """
    def __init__(self, dag, parts, partlib):
        self.dag = dag
        self.rdag = self._reverse_dag()       
        self.parts = parts
        self.partlib = partlib

        # When multiple copies of a mesh are loaded in a Blender 
        # scene (e.g. four legs, Blender puts them all into a global 
        # namespace and modifies their default name by appending 
        # '.00x'. We have to hold a counter for each name so that 
        # we can search for a name actually in a Blender scene.
        self.instance_count = defaultdict(int) 

        # Maps to hold mesh object for each semantic part name
        self.object_map = {}

    def _reverse_dag(self):
        """
        Returns the adjacency list representation of `dag` 
        with its edge directions reversed. `dag` is expected
        to be represented as an adjacency list.
        """
        reversed_dag = defaultdict(list)
        for key, vals in self.dag.items():
            for v in vals:                
                rkey = v['node']
                rval = {'node': key, 'edge': v['edge']}                                
                reversed_dag[rkey].append(rval)

        return reversed_dag 

    def _process(self, node):        
        if node == 'root':
            return

        # Load the part into the scene
        # Update instance counter if >1
        # instances present in the scene        
        part_id = self.parts[node]        
        part = self.partlib.load(part_id)
        part.instance_num = self.instance_count[part_id]
        part.update()
        self.instance_count[part_id] += 1

        # Record the name for each node with corresponding 
        # object instance
        self.object_map[node] = part

        # Attach part to parent
        parents = self.rdag[node]        
        assert len(parents) >= 1, 'No parents found for node {}'.format(node)

        if len(parents) == 1:             
            parent = parents[0]

            # If node is child of 'root', nothing further to do
            if parent['node'] == 'root':
                return        

            self._attach1(node, parent)            
        else:
            self._attach2(node, parents)       


    def _attach1(self, node, parent):
        """
        Attack child to single parent
        """
        parent_name = parent['node']
        sock_type = parent['edge']['socket']
        plug_type = parent['edge']['plug']
        # Get parent object and its socket object
        parent_part = self.object_map[parent_name]
        sock_name = parent_part['sockets'][sock_type]['names'].pop(0)        
        sock = ba.D.objects[sock_name]

        # Get the child object and its plug 
        plug_name  = self.object_map[node]['plugs'][plug_type]['names'][0]
        plug = ba.D.objects[plug_name]

        # Set parent's socket as parent of child's plug 
        plug.parent = sock

        # Clear child's origin, so it snaps to parent
        ba.OPS.object.select_all(action='DESELECT')
        plug.select_set(True)
        ba.OPS.object.origin_clear()
        
        print('attach {}:{} -> {}:{}'.format(node, plug_name, parent_name, sock_name))


    def _attach2(self, node, parents):
        """
        Attack child to multiple parents
        """
        print('attach2')
        pass


    def build(self):
        frontier = ['root']
        visited = set()

        while frontier:
            node = frontier.pop(0)
            if node in visited:
                continue

            visited.add(node)            
            self._process(node)            
            children = self.dag.get(node, None)
            if not children:
                continue

            for child in children:
                child_name = child['node']
                if child_name not in frontier:
                    frontier.append(child_name)

def main():
    ba.delete_default_objects()
    
    path = '/Users/rohan/work/code/learning/partlib/partlib'
    partlib = Partlib(path)

    parts = {
        'top': '8bf101', 
        'l0': '78bf73', 
        'l1': '78bf73', 
        'l2': '78bf73', 
        'l3': '78bf73',
        'subtop': '8ec62d'              
    }

    graph_0 = {
        'root': [{'node': 'top', 'edge': {'plug': 'plug_default', 'socket': 'sock_default'}}],
        'top': [
            {'node': 'l0', 'edge': {'plug':'plug_top', 'socket': 'sock_side'}},
            {'node': 'l1', 'edge': {'plug':'plug_top', 'socket': 'sock_side'}},
            {'node': 'l2', 'edge': {'plug':'plug_top', 'socket': 'sock_side'}},
            {'node': 'l3', 'edge': {'plug':'plug_top', 'socket': 'sock_side'}},
            {'node': 'subtop', 'edge': {'plug':'plug_top', 'socket': 'sock_center'}}
        ]
    }
    
    graph_1 = {
        'root': [{'node': 'top', 'edge': {'plug': 'plug_default', 'socket': 'sock_default'}}],
        'top': [
            {'node': 'l0', 'edge': {'plug':'plug_top', 'socket': 'sock_corner'}},
            {'node': 'l1', 'edge': {'plug':'plug_top', 'socket': 'sock_corner'}},
            {'node': 'l2', 'edge': {'plug':'plug_top', 'socket': 'sock_corner'}},
            {'node': 'l3', 'edge': {'plug':'plug_top', 'socket': 'sock_corner'}}
        ],
        'l0': [{'node': 'shelf', 'edge': {'plug':'plug_corner', 'socket': 'sock_center'}}],
        'l1': [{'node': 'shelf', 'edge': {'plug':'plug_corner', 'socket': 'sock_center'}}],
        'l2': [{'node': 'shelf', 'edge': {'plug':'plug_corner', 'socket': 'sock_center'}}],
        'l3': [{'node': 'shelf', 'edge': {'plug':'plug_corner', 'socket': 'sock_center'}}]
    }

    path = '/Users/rohan/work/code/learning/partlib/partlib'
    partlib = Partlib(path)

    builder = Builder(graph_0, parts, partlib)
    builder.build()


if __name__ == '__main__':
    main()




