# fabriclib
'fabriclib' is a generic library written in python to access and automate Cisco MDS switches

Some of the salient features of this library are:
  - Access switches via telnet or ssh
  - Access switches via NXAPI
  - Support for setting different NXAPI message formats and command types
  - Ability to discover all the switches in the fabric by using a single seed switch ip (just like DCNM)
  - Easy access to cli show command outputs by writing parsers (can be extended to NXAPI outputs as well)
  - Integrated python logging facilty for easy debugging

For examples on how to use this library head over to the examples directory 'fabriclib_examples'.  
For further queries on how to use the library or any bugs or enhancements, pls contact **Suhas Bharadwaj (subharad@cisco.com)**

