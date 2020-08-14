from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from collections import deque
import os

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def get_opposite_direction(direction):
    if direction == "n":
        return "s"
    elif direction == "s":
        return "n"
    elif direction == "e":
        return "w"
    elif direction == "w":
        return "e"
    else:
        print("INVALID DIRECTION")
        return None

# def print_room_path(rp):
#     print("[", end=" ")
#     for r in room_path:
#         if r != None:
#             print(r.id, end=" ")
#         else:
#             print(None, end=" ")
#     print("]")

# dft(starting room)
# visited rooms
rooms_visited = set()

# initialize unvisited exits count
count = 0
# create a dictionary to keep track connections between rooms
# direction : room_id if visited
# direction : ? if unvisited
rooms = {}

# create an empty stack to store room path
s = deque()
# add initial room path,  [ 0, 1 ]
s.append([world.starting_room])

# while there are unvisited exits
while count >= 0:
    # pop room path
    room_path = s.pop()
    # if not at starting room
    if len(room_path) > 1:
        # add current room 
        prev_room = room_path[-2]
        # if placeholder room
        if room_path[-1] == None:
            # change placeholder to correct current room
            room_path[-1] = room_path[-2].get_room_in_direction(traversal_path[-1])
    # current room
    cur_room = room_path[-1]
    # if room is unvisited
    if cur_room.id not in rooms_visited:
        # add room_id to visited_rooms
        rooms_visited.add(cur_room.id)
        # initialize all possible exits for current room
        for e in cur_room.get_exits():
            if cur_room.id not in rooms:
                rooms[cur_room.id] = {}
            rooms[cur_room.id][e] = '?'
        # add connection with previous room(except for starting room)
        # using last path
        if cur_room.id != world.starting_room.id:
            last_direction = traversal_path[-1]
            count -= 1
            rooms[cur_room.id][get_opposite_direction(last_direction)] = prev_room.id
            rooms[prev_room.id][last_direction] = cur_room.id
        # find unvisited exits, create unknown exits
        exits = []
        for d in list(rooms[cur_room.id]):
            # if exit is unknown, increment count
            if rooms[cur_room.id][d] == "?":
                # add to traversal path
                exits.append(d)
                count += 1
        # if there are unknown exits
        if len(exits) > 0:
            # add new direction
            traversal_path.append(exits[0])
            # add placeholder for new room
            new_room_path = list(room_path)
            new_room_path.append(None)
            # append new room path
            s.append(new_room_path)
        # no exits other than opposite of last direction
        else:
            # go back
            traversal_path.append(get_opposite_direction(traversal_path[-1]))
            # add last path to stack
            new_room_path = list(room_path)
            new_room_path.pop()
            s.append(new_room_path)
    # if room is visited
    else:
        # create unknown exits
        exits = []
        for d in list(rooms[cur_room.id]):
            # if exit is unknown, increment count
            if rooms[cur_room.id][d] == "?":
                # if prev room is connected to current room and is not starting room
                if get_opposite_direction(d) in rooms[prev_room.id] and len(room_path) > 1 and prev_room.id not in rooms[cur_room.id].values():
                    if rooms[prev_room.id][get_opposite_direction(d)] == "?":
                        rooms[cur_room.id][d] = prev_room.id
                        rooms[prev_room.id][get_opposite_direction(d)] = cur_room.id
                    else:
                        # add to traversal path
                        exits.append(d)
                # prev room is not connected to current room or current room is starting room
                else:
                    # add to traversal path
                    exits.append(d)
        # if there are unknown exits
        if len(exits) > 0:
            # add new direction
            traversal_path.append(exits[0])
            # add placeholder for new room
            new_room_path = list(room_path)
            new_room_path.append(None)
            # append new room path
            s.append(new_room_path)
        # no exits other than opposite of last direction
        else:
            # add last path to stack
            new_room_path = list(room_path)
            # if not at starting room
            if len(new_room_path) > 1:
                new_room_path.pop()
            else:
                break
            # go back to last room in room path
            for (d, r) in list(rooms[cur_room.id].items()):
                # find right direction to go back
                if r == new_room_path[-1].id:
                    traversal_path.append(d)
            # add back path to room path
            s.append(new_room_path)

    # print("count: ", count)
    # print("travel: ", len(traversal_path))
    # print(traversal_path)
    # if cur_room.id == 8:
    #     os.system("pause")
    # if len(traversal_path) == 6:
    #     os.system("pause")

# print(len(rooms_visited))
# print(len(traversal_path))

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
