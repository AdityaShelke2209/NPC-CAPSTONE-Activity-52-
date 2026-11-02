# Cryptographic Hash Results and Integrity Analysis

**Student Name:** Aditya Arun Shelke  
**PRN:** 2125UCSM1052  
**Course:** B.Tech Computer Science Engineering (Cyber Security)  
**Institution:** Sanjivani University, Kopargaon  
**Subject:** NPC Capstone Project  
**Academic Year:** 2026–2027  

---

## 1. The Role of Cryptographic Hashing in Malware Analysis

Cryptographic hash functions map arbitrary-length binary inputs into fixed-length digest strings. In malware analysis and incident response, cryptographic hashing provides five core capabilities:

1. **Deterministic Unique Fingerprinting:** A file produces an identical hash digest whenever processed by the same algorithm.
2. **Avalanche Effect:** Altering even a single bit or whitespace character in the script completely alters the resulting digest, exposing any tampering.
3. **Collision Resistance:** Computationally infeasible for two distinct files to generate the identical SHA-256 hash digest.
4. **Indicator of Compromise (IoC) Sharing:** Threat intelligence platforms (VirusTotal, AlienVault OTX, MISP) catalog malware by SHA-256 rather than file names, which are trivial for attackers to rename.
5. **Chain of Custody & Forensic Verification:** Proves that an evidence sample remained unmodified from the moment of initial triage to final reporting.

---

## 2. Calculated Cryptographic Hashes

The following hashes were computed directly from the laboratory scripts using SHA-256, SHA-1, and MD5 algorithms:

### Laboratory Server Script (`server.py`)
- **File Path:** `lab/safe_shell_simulation/server.py`
- **File Size:** `6,841 bytes`
- **MD5:** `6e36548c4b8dc744501b625a29a421fd`
- **SHA-1:** `52fce0eda06fe5d2154a318f50ed2999b2f28a2f`
- **SHA-256:**
  ```
  a7a46232ddd918b56a2b656028fb024eccebdfd681cd05bb3f1a2f4c26098609
  ```

### Laboratory Client Script (`client.py`)
- **File Path:** `lab/safe_shell_simulation/client.py`
- **File Size:** `2,814 bytes`
- **MD5:** `6d6fb7393a31e632dbf44743cfe1d352`
- **SHA-1:** `2a83ba6191c450ec780ad18de006dae4a9c5ce66`
- **SHA-256:**
  ```
  18ac3d4d60d01c33322a70036c1820768e7d3fc0bc37b3e60ad503236ac8f1fa
  ```

---

## 3. How to Calculate and Verify in Linux

Inside the Linux virtual machine terminal, compute and verify the hashes using standard core utilities:

```bash
# Calculate SHA-256 hash
sha256sum lab/safe_shell_simulation/server.py

# Calculate SHA-1 hash
sha1sum lab/safe_shell_simulation/server.py

# Calculate MD5 hash
md5sum lab/safe_shell_simulation/server.py
```

### Integrity Verification File
You can export the hashes to an integrity manifest:
```bash
sha256sum lab/safe_shell_simulation/*.py > checksums.sha256
sha256sum -c checksums.sha256
```
*Expected Output:*
```
lab/safe_shell_simulation/server.py: OK
lab/safe_shell_simulation/client.py: OK
```
