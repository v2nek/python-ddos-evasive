python-ddos-evasive
===================

Small script to analyze access log and block bad IP's.
I was inspired by evasive.pl script, but it was too slow to handle all logs that i recieve.
Just mine small app that helped me to mitigate lots of attacks.

You will find nginx log configuration in nginx.log.conf.
Also you will need ipset. On debian you can set it up with m-a a-i ipset.

To increase performance you can compile this script to bin file with pyinstaller.