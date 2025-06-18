import psutil

def detectNic() -> list[str]:
    """
       Returns a list of active network interfaces using psutil library.
       This will be used for socket.bind()
    """

    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    active_interfaces = [
        iface for iface in interfaces
        if iface in stats and stats[iface].isup
    ]

    return active_interfaces