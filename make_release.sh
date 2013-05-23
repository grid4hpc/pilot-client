#!/bin/sh

ssh shamardin@tb01.ngrid.ru "svn co https://svn.ngrid.ru/pilot/trunk/pilot_cli pilot_cli_build"
rsync -avzP ext_dist/*.gz ext_dist/*.py ext_dist/*.egg shamardin@tb01.ngrid.ru:pilot_cli_build/ext_dist/
ssh shamardin@tb01.ngrid.ru "cd pilot_cli_build ; rm -rf dist/ ; ./mkdist.sh"
release_name=`ssh shamardin@tb01.ngrid.ru "cd pilot_cli_build/dist ; ls -1 *.tar.gz"`
echo "Built release $release_name"
echo "Upload to server? Press enter or Ctrl-C"
read X
scp shamardin@tb01.ngrid.ru:pilot_cli_build/dist/$release_name /tmp/$release_name
scp /tmp/$release_name root@www.ngrid.ru:/srv/web/www/html/sw/pilot_cli/
echo "Uploaded $release_name to http://www.ngrid.ru/sw/pilot_cli/$release_name"
