---
title: "C# Socket Close() vs Disconnect()"
date: 2020-07-25T19:00:40-14:00
categories:
  - blog, c#, notes
tags:
  - c++
  - notes
  - draft
---
## .Net ```Socket.Close()``` sends ```RST``` flag in instead of ```FIN/ACK```


While working TCP implementation, I could not understand why ```Socket.close()``` method was not working as expected.
Expected means the in connection orriented protocol the close() method should be graceful. It should send all the pendinfg resources.
It should not shutdhown in the middle. I was checking if I have received all the data. Then using Wireshark, could find the couse that
insteam if sending ``FIN/ACK```  I was sending "RST" packet.
After few trial and error, figured out that ```Socket.Disconnect(false)``` sends "FIN/ACK".

C# Close() https://docs.microsoft.com/en-us/dotnet/api/system.net.sockets.socket.close?redirectedfrom=MSDN&view=netcore-3.1

TPC flow: https://www.ibm.com/support/knowledgecenter/SSB23S_1.1.0.2020/gtps7/s5tcpcf.html

