# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from configman import Namespace
from socorro.cron.crontabber import BaseCronApp


class FooCronApp(BaseCronApp):
    app_name = 'foo'
    app_description = 'Does some foo things'

    required_config = Namespace()
    # e.g.
    #required_config.add_option(
    #    'my_option',
    #    default='Must have a default',
    #    doc='Explanation of the option')

    def run(self):
        print "DOING STUFF foo()"
