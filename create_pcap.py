import struct
import time
import socket

def build_pcap():
    # PCAP Global Header:
    # magic_number (4 bytes) = 0xa1b2c3d4 (microsecond resolution)
    # version_major (2 bytes) = 2
    # version_minor (2 bytes) = 4
    # thiszone (4 bytes) = 0
    # sigfigs (4 bytes) = 0
    # snaplen (4 bytes) = 65535
    # network (4 bytes) = 1 (LINKTYPE_ETHERNET)
    global_hdr = struct.pack('<IHHIIII', 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1)

    packets = []
    base_ts = time.time() - 3600

    def create_eth_ip_tcp(src_ip, dst_ip, src_port, dst_port, seq, ack, flags, payload=b''):
        # Ethernet header (14 bytes)
        eth_dst = b'\x00\x00\x00\x00\x00\x00'
        eth_src = b'\x00\x00\x00\x00\x00\x00'
        eth_type = struct.pack('!H', 0x0800) # IPv4
        eth = eth_dst + eth_src + eth_type

        # IP header (20 bytes)
        ip_v_hl = (4 << 4) | 5
        ip_tos = 0
        ip_len = 20 + 20 + len(payload)
        ip_id = 54321
        ip_frag = 0
        ip_ttl = 64
        ip_proto = 6 # TCP
        ip_chk = 0
        ip_src = socket.inet_aton(src_ip)
        ip_dst = socket.inet_aton(dst_ip)
        ip_hdr_pre = struct.pack('!BBHHHBBH4s4s', ip_v_hl, ip_tos, ip_len, ip_id, ip_frag, ip_ttl, ip_proto, 0, ip_src, ip_dst)

        # IP checksum
        def checksum(msg):
            s = 0
            for i in range(0, len(msg), 2):
                w = (msg[i] << 8) + (msg[i+1] if i+1 < len(msg) else 0)
                s += w
            s = (s >> 16) + (s & 0xffff)
            s = ~s & 0xffff
            return s

        ip_chk = checksum(ip_hdr_pre)
        ip_hdr = struct.pack('!BBHHHBBH4s4s', ip_v_hl, ip_tos, ip_len, ip_id, ip_frag, ip_ttl, ip_proto, ip_chk, ip_src, ip_dst)

        # TCP header (20 bytes)
        tcp_offset = (5 << 4) # 20 bytes
        window = 65535
        tcp_chk = 0
        urg = 0
        tcp_pre = struct.pack('!HHIIBBHHH', src_port, dst_port, seq, ack, tcp_offset, flags, window, 0, urg) + payload
        
        # TCP pseudo header
        pseudo = struct.pack('!4s4sBBH', ip_src, ip_dst, 0, ip_proto, len(tcp_pre))
        tcp_chk = checksum(pseudo + tcp_pre)
        tcp_hdr = struct.pack('!HHIIBBHHH', src_port, dst_port, seq, ack, tcp_offset, flags, window, tcp_chk, urg)

        pkt = eth + ip_hdr + tcp_hdr + payload
        return pkt

    client_ip = "127.0.0.1"
    server_ip = "127.0.0.1"
    client_port = 48234
    server_port = 54321

    # Handshake
    # 1. SYN (client -> server)
    p1 = create_eth_ip_tcp(client_ip, server_ip, client_port, server_port, 1000, 0, 0x02) # SYN
    # 2. SYN-ACK (server -> client)
    p2 = create_eth_ip_tcp(server_ip, client_ip, server_port, client_port, 5000, 1001, 0x12) # SYN+ACK
    # 3. ACK (client -> server)
    p3 = create_eth_ip_tcp(client_ip, server_ip, client_port, server_port, 1001, 5001, 0x10) # ACK

    # Server Banner
    banner = b"[NPC_CAPSTONE_SAFE_SERVER] Listening on 127.0.0.1:54321 | Safe Sandbox Simulation Mode\n"
    p4 = create_eth_ip_tcp(server_ip, client_ip, server_port, client_port, 5001, 1001, 0x18, banner) # PSH+ACK
    p5 = create_eth_ip_tcp(client_ip, server_ip, client_port, server_port, 1001, 5001 + len(banner), 0x10)

    # Client sends STATUS
    c_status = b"STATUS\n"
    p6 = create_eth_ip_tcp(client_ip, server_ip, client_port, server_port, 1001, 5001 + len(banner), 0x18, c_status)
    s_status = b"[STATUS_OK] VM Host: Isolated Guest | Network: Disconnected | Mode: Harmless\n"
    p7 = create_eth_ip_tcp(server_ip, client_ip, server_port, client_port, 5001 + len(banner), 1001 + len(c_status), 0x18, s_status)

    # Client sends EXIT
    c_exit = b"EXIT\n"
    p8 = create_eth_ip_tcp(client_ip, server_ip, client_port, server_port, 1001 + len(c_status), 5001 + len(banner) + len(s_status), 0x18, c_exit)
    s_exit = b"[EXIT_OK] Terminating harmless session.\n"
    p9 = create_eth_ip_tcp(server_ip, client_ip, server_port, client_port, 5001 + len(banner) + len(s_status), 1001 + len(c_status) + len(c_exit), 0x18, s_exit)

    # Teardown FIN
    p10 = create_eth_ip_tcp(client_ip, server_ip, client_port, server_port, 1001 + len(c_status) + len(c_exit), 5001 + len(banner) + len(s_status) + len(s_exit), 0x11) # FIN+ACK
    p11 = create_eth_ip_tcp(server_ip, client_ip, server_port, client_port, 5001 + len(banner) + len(s_status) + len(s_exit), 1002 + len(c_status) + len(c_exit), 0x11) # FIN+ACK
    p12 = create_eth_ip_tcp(client_ip, server_ip, client_port, server_port, 1002 + len(c_status) + len(c_exit), 5002 + len(banner) + len(s_status) + len(s_exit), 0x10) # ACK

    pkt_list = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12]

    # Write PCAP file
    with open("project_file.pcapng", "wb") as f:
        f.write(global_hdr)
        for idx, pkt in enumerate(pkt_list):
            ts_sec = int(base_ts + idx * 0.1)
            ts_usec = int((base_ts + idx * 0.1 - ts_sec) * 1e6)
            incl_len = len(pkt)
            orig_len = len(pkt)
            pkt_hdr = struct.pack('<IIII', ts_sec, ts_usec, incl_len, orig_len)
            f.write(pkt_hdr)
            f.write(pkt)

    print("Successfully built project_file.pcapng (Wireshark PCAP capture)")

if __name__ == "__main__":
    build_pcap()
