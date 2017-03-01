# Project Basecamp
Metasploit modules developed to demonstrate insecure by design PLC's as part of Project Basecamp. See [Dale Peterson's Introduction to Basecamp Video](https://www.youtube.com/watch?v=BKJje3Ram2I&t=9s)

Project Basecamp is a research effort by Digital Bond and a team of volunteer researchers to highlight and demonstrate the fragility and insecurity of most SCADA and DCS field devices, such as PLC's and RTU's.

The goal of Project Basecamp is to make the risk of these fragile and insecure devices so apparent and easy to demonstrate that a decade of inaction will end. SCADA and DCS owner/operators will demand a secure and robust PLC, and this will drive vendors to finally provide a product worthy of being deployed in the critical infrastructure.

## The Reason: A Firesheep Moment for PLC's

Everyone knows PLC's are vulnerable --- or so we have heard for ten years now since the 9/11 attacks focused attention on DCS and SCADA security. Not only do they lack basic security features, they are also fragile. Warnings abound about the dangers of even running a port scan on a PLC. Yet even though "everyone knows" there has been little or no progress on developing even the option of purchasing a secure and robust PLC.

After this lost decade, Digital Bond decided to stop trying the same failed approach and the result is Project Basecamp. We looked for parallel situations in security where a serious problem was known, not addressed for a long time, and then something triggered a change. The best example we found is Firesheep.

In 2007/2008 there were numerous presentations at security events showing how a twitter, facebook, gmail or other HTTP session could be hijacked because the cookies were not encrypted. It got some buzz at a security events and technical web sites, but no action to address the vulnerability.

In October of 2010 Eric Butler created Firesheep, an easy to use Firefox extension that hijacked an HTTP session. Anyone who could use a browser could hijack Facebook or Twitter sessions in a coffee shop. Shortly after that the vendors took action and made mandatory HTTPS an option and eventually the default.

Project Basecamp is attempting to be a Firesheep Moment for PLC's. The team has, not surprisingly, found many vulnerabilities in the PLC's, but perhaps more importantly have identified "insecure by design" issues that are actually much easier to leverage to affect the availability and integrity of a process.

The key to making this a Firesheep Moment for PLC's is providing tools so any engineer, IT type, security professional or anyone with a bit of computer skill can demonstrate just how fragile and vulnerable these PLC's are. It's beyond, PLC's are vulnerable. Basecamp provides the tools to show an executive just how easy it is to take down the SCADA or DCS.

## The Basecamp Team

Reid Wightman of Digital Bond leads the Basecamp team. He performed the work on two of the devices and coordinated the results with the rest of the research team. The other Project Basecamp team members are:

- Dillon Beresford
- Jacob Kitchel
- Ruben Santamarta
- Anonymous 1
- Anonymous 2

## The Results

We have created individual pages for the PLC / Controllers with Project Basecamp modules.

- 3S CoDeSys
- General Electric D20ME
