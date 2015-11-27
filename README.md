# teleops
Talk to your servers in real time! TeleOps facilitates shell and management console access through instant messaging infrastructure.

TeleOps

WRAP OPEN IM API (e.g. telegram et al)  with python server infra. for notification and response to ops alrets in your palm.

Relevant links: 

* http://flask.pocoo.org/ (https://github.com/tgalal/yowsup)
* https://twistedmatrix.com/trac/
* https://github.com/sivang/navistore (for reference)
* https://telegram.org/
* http://www.fabfile.org/
* telegram: https://pypi.python.org/pypi/python-telegram-bot
* hangouts: https://github.com/hangoutsbot/hangoutsbot

Post: When on call, I'd always wanted to be able to get critical notifications and act upon them via Instant Messaging.
Owner: Sivan 
Wish to join: Ishay Michal 
Proposed Implementation Plan: 
Using Navistore as reference, we could create REST end points for accepting incoming notifications from monitoring solutions  (like Sensu et al and statsd)  such that they will be delivered to an on call engineer. Upon receipt, an engineer can respond to critical alerts with text that actually denotes commands (be it investigative, or corrective) , to be executed at the alerting instance, every alerts/response duo should be recorded and maintained as a scenario accessible to the whole on call rotation team. This allows for every on call engineer to continue each other's work and have a log of actions for cases when problem that has been deemed 'solved' is re-experienced.
Such case documentation would enable better knowledge flow based on events happening through arbitrary time frame in the on-duty engineering life cycle.
 
Hackathon Aftermath:

* Use slack's API for real time messaging that is actually tailored to this sort of use cases as per:
    * https://api.slack.com/bot-users
    * https://api.slack.com/rtm
    * Slack's is already well known in the Ops communities and is widely used to consolidate alerts, notifications and events - quick almost free-to-bite event propagation support, ACLs and granular user management.
* Use an event IO framework  (see Navistore's HTTP server)  to actually build a robust parent process allowing for:
    * Killing long running commands that have not returned reaching a preset timeout.
    * Robustness of the main event loop such that no command can halt main process but still an update would be sent to the user of the situation.
* Perhaps alternatively or in combination use pyzmq to make command execution even more robust allowing orchestration of multiple commands per user, employing worker process model isolating failures to childs making parent/controller process virtually bullet proof within the limitation of an affected system (e.g. severe memory shortage would render even such architecture DOS'd)
* Whenever embarking on a new project idea, always make sure you've exhausted search for existing building blocks that can be reused or are completely unsuitable before coding it yourself, to avoid NIH. Consider https://www.duosecurity.com/product/methods/duo-mobile for 2 factor authentication (thanks to Shahar Mintz for bringing this to my attention).

By Sivan Greenberg, Ishay Peled and Michal Kelner Mishali.

