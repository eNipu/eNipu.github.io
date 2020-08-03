---
title: "C# Socket close() vs disconnect()"
date: 2020-07-25T19:00:40-14:00
categories:
  - blog, c#, notes
tags:
  - c++
  - notes
  - draft
---
## .Net ```Socket.close()``` send ```RST``` flag in instead of FIN/ACK

https://docs.microsoft.com/en-us/dotnet/api/system.net.sockets.socket.close?redirectedfrom=MSDN&view=netcore-3.1
While working TCP implementation, I could not understand why ```Socket.close()``` method was sending RST packet.
https://www.ibm.com/support/knowledgecenter/SSB23S_1.1.0.2020/gtps7/s5tcpcf.html

