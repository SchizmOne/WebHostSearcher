def get_tcp_ports():
    ports = {
        21: "ftp",
        22: "ssh",
        23: "telnet",
        25: "smtp",
        53: "domain",
        80: "http",
        81: "http",
        110: "pop3",
        443: "https",
        465: "smtps",
        515: "printer",
        631: "ipp",
        8080: "http-local"
    }
    return ports
