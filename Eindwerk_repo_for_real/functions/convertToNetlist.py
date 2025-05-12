from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
import platform
import matplotlib.pyplot as plt
import os
from tkinter import Tk, messagebox
from collections import defaultdict, deque

def simulate(components, connections):
    Tk().withdraw()
    circuit = Circuit("Simulated Circuit")
    print("🖥️ Architecture:", platform.architecture())

    pin_to_node = {}
    node_counter = 1

    def get_or_create_node(pos):
        if pos is None:
            return "0"
        pos = tuple(pos)
        for existing_pos in pin_to_node:
            if abs(pos[0] - existing_pos[0]) < 1e-3 and abs(pos[1] - existing_pos[1]) < 1e-3:
                return pin_to_node[existing_pos]
        nonlocal node_counter
        pin_to_node[pos] = f"N{node_counter}"
        node_counter += 1
        return pin_to_node[pos]

    SPICE_MAP = {
        "Resistor": ("R", "Ohm"),
        "Capacitor": ("C", "Farad"),
        "Inductor": ("L", "Henry"),
        "DC_Voltage_Src": ("V", "Voltage"),
        "Battery": ("V", "Voltage"),  # Battery treated as Voltage Source
        "Diode": ("D", "Model"),
        "Ground": ("GND", None),
    }

    def get_property(properties, key):
        for k, v in properties:
            if k.lower() == key.lower():
                return v
        return None

    # Step 1: Identify all explicit ground positions
    ground_positions = []
    for comp in components:
        if type(comp).__name__ == "Ground":
            if comp.pos_pin1:
                pin_to_node[tuple(comp.pos_pin1)] = "0"
                ground_positions.append(tuple(comp.pos_pin1))

    # Special case: for Battery, treat pos_pin1 as ground
    for comp in components:
        if type(comp).__name__ == "Battery":
            if comp.pos_pin1:
                pin_to_node[tuple(comp.pos_pin1)] = "0"
                ground_positions.append(tuple(comp.pos_pin1))

    # Step 2: Build graph of connected positions
    connection_graph = defaultdict(set)
    for conn in connections:
        if conn.start_pos and conn.end_pos:
            start = tuple(conn.start_pos)
            end = tuple(conn.end_pos)
            connection_graph[start].add(end)
            connection_graph[end].add(start)

    # Step 3: Propagate "0" (ground) to all connected positions
    visited = set()
    ground_queue = deque(ground_positions)
    while ground_queue:
        current = ground_queue.popleft()
        visited.add(current)
        for neighbor in connection_graph[current]:
            if neighbor not in visited:
                pin_to_node[neighbor] = "0"
                ground_queue.append(neighbor)

    # Step 4: Assign nodes to remaining positions
    for conn in connections:
        if conn.start_pos and conn.end_pos:
            start = tuple(conn.start_pos)
            end = tuple(conn.end_pos)
            if start not in pin_to_node and end in pin_to_node:
                pin_to_node[start] = pin_to_node[end]
            elif end not in pin_to_node and start in pin_to_node:
                pin_to_node[end] = pin_to_node[start]
            elif start not in pin_to_node and end not in pin_to_node:
                node = get_or_create_node(start)
                pin_to_node[start] = node
                pin_to_node[end] = node

    # Step 5: Map components to circuit
    for comp in components:
        class_name = type(comp).__name__
        name = comp.name
        pin1 = comp.pos_pin1
        pin2 = comp.pos_pin2
        props = comp.properties

        if class_name not in SPICE_MAP:
            print(f"⚠️ Unsupported: {name} ({class_name})")
            continue

        prefix, prop_key = SPICE_MAP[class_name]

        if class_name == "Ground":
            continue

        node1 = pin_to_node.get(tuple(pin1), get_or_create_node(pin1))
        node2 = pin_to_node.get(tuple(pin2), get_or_create_node(pin2))

        value = get_property(props, prop_key)
        if value is None:
            print(f"⚠️ Missing property '{prop_key}' for {name}")
            continue

        if prefix == "R":
            circuit.R(name, node1, node2, float(value))
        elif prefix == "C":
            circuit.C(name, node1, node2, float(value))
        elif prefix == "L":
            circuit.L(name, node1, node2, float(value))
        elif prefix == "V":
            if class_name == "Battery":
                # For Battery, extract voltage property
                battery_voltage = get_property(props, "Voltage")
                if battery_voltage is not None:
                    # Create a DC voltage source for the battery with 'DC' explicitly mentioned
                    circuit.V(name, node1, node2, dc_value=float(battery_voltage))  # Add DC explicitly
                else:
                    print(f"⚠️ Missing voltage property for Battery: {name}")
            else:
                circuit.V(name, node1, node2, float(value))  # For other voltage sources
        elif prefix == "D":
            circuit.model("Dmodel", "D")
            circuit.D(name, node1, node2, model="Dmodel")

    # Save the netlist
    os.makedirs("netlists", exist_ok=True)
    netlist_path = os.path.join("netlists", "generated_netlist.cir")
    with open(netlist_path, "w") as f:
        f.write(str(circuit))
    print("📝 Netlist saved to:", netlist_path)
    print("🧾 Netlist content:\n", str(circuit))

    # Run the simulation
    try:
        simulator = circuit.simulator(temperature=25, nominal_temperature=25)
        analysis = simulator.transient(step_time=1@u_us, end_time=10@u_ms)

        # Plot results
        plt.figure("SPICE Simulation")
        for node in set(pin_to_node.values()):
            try:
                if node in analysis.nodes:
                    plt.plot(analysis.time, analysis[node], label=node)
            except Exception as e:
                print(f"⚠️ Could not plot {node}: {e}")

        plt.title("SPICE Simulation")
        plt.xlabel("Time (s)")
        plt.ylabel("Voltage (V)")
        plt.legend()
        plt.grid(True)
        plt.show()

    except Exception as e:
        messagebox.showerror("Simulation Error", f"❌ Simulation failed:\n{e}")
        print(f"❌ Simulation failed: {e}")

    print("✅ Simulation complete.")
