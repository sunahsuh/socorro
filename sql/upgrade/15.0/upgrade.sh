#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

#please see README

set -e

CURDIR=$(dirname $0)
DBNAME=$1
: ${DBNAME:="breakpad"}
VERSION=15.0

echo '*********************************************************'
echo 'add field to track auto refresh date'
echo 'bug 768300'
psql -f ${CURDIR}/create_refresh_date.sql $DBNAME

#change version in DB
psql -c "SELECT update_socorro_db_version( '$VERSION' )" $DBNAME

echo "$VERSION upgrade done"

exit 0