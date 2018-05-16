echo off
set ldap_url=%1
set name=%2
set output=%3
set error=%4
ldapsearch -b ou=people,o=nsn -h %ldap_url% -x -X -p 389 uid=%name% 1>>%output% 2>>%error%