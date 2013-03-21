# Sentry on Dotcloud

Forked from the excellent [original work from dotcloud](https://github.com/dotcloud/sentry-on-dotcloud).

## Changes from original

* Latest software versions (requirements.txt)
* This README

## Getting started

Edit the configuration in `dotcloud.yml`:

* SENTRY_URL_PREFIX : URL of sentry when deployed (should be `sentry-<dotcloud_username>.dotcloud.com`)
* SENTRY_WEB_ADMIN : admin username in sentry
* SENTRY_WEB_ADMIN_PASSWORD : admin password in sentry
* SENTRY_KEY : a unique key
* SENTRY_ADMIN : your email for internal errors notifications

Get started with Dotcloud <http://docs.dotcloud.com/firststeps/install/>

Once you install and configured the Dotcloud cli:

	git clone git@github.com:abulte/sentry-on-dotcloud.git
	cd sentry-on-dotcloud
	dotcloud create sentry # answer Y
	dotcloud push
	
And after a while, it's done! The cli gives you the URL you should visit.