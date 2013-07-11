#!/bin/bash

echo `date` "all  $1 $2 $3" >> /var/log/ipset/ipset.log
ipset -q -A all $1 --timeout 1800
