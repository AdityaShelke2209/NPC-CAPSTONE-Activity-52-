# Laboratory Screenshots & Evidence

**Student Name:** Aditya Arun Shelke  
**PRN:** 2125UCSM1052  
**Subject:** NPC (Unit 1)  
**Institution:** Sanjivani University, Kopargaon  

---

### Screenshot Catalog

| Figure | Description | File |
| :---: | :--- | :--- |
| **Fig 01** | VM Hardware Specifications Dialog (RAM, vCPU, Storage) | `fig01_vm_configuration.png` |
| **Fig 02** | Network Adapter Isolation Settings (Disconnected / Host-Only) | `fig02_network_isolation.png` |
| **Fig 03** | Linux Guest Desktop & Boot Verification | `fig03_linux_guest_boot.png` |
| **Fig 04** | Empirically Verified Internet Isolation (`ping 8.8.8.8` & `ip route`) | `fig04_internet_isolation_test.png` |
| **Fig 05** | Clean Snapshot in Snapshot Manager (`NPC_Capstone_Clean_State`) | `fig05_clean_snapshot_manager.png` |
| **Fig 06** | Baseline Process & Socket Triage (`ps aux`, `ss -tulpn`) | `fig06_baseline_processes_ports.png` |
| **Fig 07** | Safe Server Launch on Loopback (`python3 server.py`) | `fig07_server_launch.png` |
| **Fig 08** | Listening Socket Verification (`ss -tulpn \| grep 54321`) | `fig08_listening_socket_ss.png` |
| **Fig 09** | Safe Client Interaction (`STATUS`, `HELP`, `EXIT`) | `fig09_client_interaction.png` |
| **Fig 10** | Active Process Triage During Run (`ps -ef \| grep server.py`) | `fig10_process_monitoring_ps.png` |
| **Fig 11** | Loopback Traffic Capture (`tcpdump -i lo port 54321`) | `fig11_loopback_pcap_tcpdump.png` |
| **Fig 12** | File Identification & Attributes (`file server.py`, `ls -la`) | `fig12_file_identification_stat.png` |
| **Fig 13** | Cryptographic SHA-256 Calculation (`sha256sum`) | `fig13_sha256_calculation.png` |
| **Fig 14** | VirusTotal Hash Lookup Query | `fig14_virustotal_hash_lookup.png` |
| **Fig 15** | Snapshot Reversion to Clean Baseline State | `fig15_snapshot_restoration.png` |
| **Fig 16** | Post-Restoration Clean System Audit | `fig16_post_restoration_audit.png` |
