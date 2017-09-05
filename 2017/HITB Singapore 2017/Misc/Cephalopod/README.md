Cephalopod

After opening the file in Wireshark and searching for flag in the data, you find a flag.png. This probably means that the flag is in the form of a PNG. Thus, simply search for the PNG signature (beginning and end) and then combine all the TCP packets that are between the signatures.