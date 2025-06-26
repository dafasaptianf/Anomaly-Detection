#!/usr/bin/env python


from .packet_direction import PacketDirection


def get_packet_flow_key(packet, direction) -> tuple:
    """Creates a key signature for a packet.

    Summary:
        Creates a key signature for a packet so it can be
        assigned to a flow.

    Args:
        packet: A network packet
        direction: The direction of a packet

    Returns:
        A tuple of the String IPv4 addresses of the destination,
        the source port as an int,
        the time to live value,
        the window size, and
        TCP flags.

    """
    if not packet.haslayer('IP'):
        return None  # Atau raise ValueError("Packet is not IP")
    
    try:
        if packet.haslayer('TCP'):
            protocol = "TCP"
        elif packet.haslayer('UDP'):
            protocol = "UDP"
        elif packet.haslayer('ICMP'):
            protocol = "ICMP"
        else:
            return None  # Protocol tidak didukung

        ip_layer = packet['IP']
        
        if direction == PacketDirection.FORWARD:
            dest_ip = ip_layer.dst
            src_ip = ip_layer.src
            if protocol == "ICMP":
                src_port = 0
                dest_port = 0
            else:
                src_port = packet[protocol].sport
                dest_port = packet[protocol].dport
        else:
            dest_ip = ip_layer.src
            src_ip = ip_layer.dst
            if protocol == "ICMP":
                src_port = 0
                dest_port = 0
            else:
                src_port = packet[protocol].dport
                dest_port = packet[protocol].sport

        return (dest_ip, src_ip, src_port, dest_port)

    except Exception as e:
        print(f"Error processing packet: {e} | {packet.summary()}")
        return None
