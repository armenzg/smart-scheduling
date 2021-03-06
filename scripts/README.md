# ETL scripts

In this directory, we will have various scripts that we can schedule via Taskcluster.

## Requirements

Requirements are specific to each script, hopefully there is `README.md` there to guide you

## Making a new script

Create a new directory and place your desired script in there.
You can define your own requirements file as well.

## Using secrets

In Taskcluster we can store [secrets](https://community-tc.services.mozilla.com/secrets).
If you belong to the [CI-A Github team](https://github.com/orgs/mozilla/teams/cia/members) team you can create and fetch secrets.
Open [this secret](https://community-tc.services.mozilla.com/secrets/project%2Fcia%2Fgarbage%2Ffoo) and try to see it. 

> You should make a test secret to ensure you have the permissions to do so

## Using secrets locally 

There is some documentation about [setup of a taskcluster client](https://github.com/taskcluster/taskcluster/tree/master/clients/client-py#setup).  The specifics are below

#### Login

You must have a github account to login to the community cluster

    https://community-tc.services.mozilla.com

#### Make a client

To get secrets, your script will require a client id and a corresponding access token. Start the process here: [Create client](https://community-tc.services.mozilla.com/auth/clients/create?scope=)

Fill in the parameters:

* **Client ID** - whatever you like, but must be prefixed with your user id. Example: `github/2334429|klahnakoski/test-id2`
* **Expires** - set up to 30 days (*default 5 minutes*)
* **Scope** - `secrets:get:project/cia/*`
   
When you save, you will get an access token. *Ensure you record the `accessToken`, you will not see it again*

#### Direct Injection

You now With the three parameters known you can get the secrets

```python
import taskcluster
options = {
    "credentials": {
        "accessToken": "nOtalEgItImAtEbAsE64aCCeStOkEnTWWxdUxbvtiI7Q",
        "clientId": "github/2334429|klahnakoski/test-id"
    },
    "rootUrl": "https://community-tc.services.mozilla.com"
}
print(taskcluster.Secrets(options))
```

#### Using environment variables

Alternatively, `optionsFromEnvironment()` can pull parameters from environment variables. Set the variables:

    set TASKCLUSTER_ROOT_URL=https://community-tc.services.mozilla.com
    set TASKCLUSTER_CLIENT_ID=github/2334429|klahnakoski/test-id;
    set TASKCLUSTER_ACCESS_TOKEN=nOtalEgItImAtEbAsE64aCCeStOkEnTWWxdUxbvtiI7Q

> Full list of [taskcluster environment variables](https://docs.taskcluster.net/docs/manual/design/env-vars) 

and use them 

```python
import taskcluster
options = taskcluster.optionsFromEnvironment()
secrets = taskcluster.Secrets(options)
print(secrets.get("project/cia/garbage/foo"))
```

## Schedule a task on Taskcluster

For now, we will have to create a hook per script and we will have to create it by hand.
You can see [this hook](https://community-tc.services.mozilla.com/hooks/project-cia/hello-world) as
a simple example. It checks out this repo, set ups the virtualenv and executes the script.

Copy the contents of that hook and create a new hook. Only modify the `command` entry to meet your needs.
Adjust the `cron` schedule in the UI.

Note that you can manually trigger a hook (without waiting for its schedule) and that will schedule a task
executing the contents of the hook.

In the future, if we decide that we want to improve this system we can define our hooks in this repo and
get them deployed automatically rather manually defining them (filed [issue](https://github.com/armenzg/smart-scheduling/issues/2)).











### Retrieving secrets locally (linux only)

To test *locally* that your script can fetch secrets you will have to [download a binary](https://github.com/taskcluster/taskcluster/tree/master/clients/client-shell#readme)
to set up your credentials. Unfortunately, this only works for Linux (filed [issue](https://github.com/armenzg/smart-scheduling/issues/1)).

On Mac OS X, you will need to right click the binary and Open it. That will except the binary from some security measures.

Once you run the following you will be signed in through the browser and it will set some TASKCLUSTER_* env variables
in your shell which are needed to authenticate:

```shell
export TASKCLUSTER_ROOT_URL=https://community-tc.services.mozilla.com
eval `~/Desktop/taskcluster signin`
```

This is a code snippet that shows you how a secret is fetched using env variables defined by the previous step:

```python
import taskcluster
# This will read the environment variables and authenticate you
secrets = taskcluster.Secrets(taskcluster.optionsFromEnvironment())
secret = secrets.get("project/cia/garbage/foo")
print(secret["secret"])
```

## How this is set up

We set up a CI-A project in the Taskcluster Community set up (see [configuration](https://github.com/mozilla/community-tc-config/blob/master/config/projects/cia.yml)).
It's documentation is defined in [here](https://github.com/mozilla/community-tc-config/blob/master/config/projects/README.md).

## Official documentation

You can find the official documentation here:

* Hooks - [docs](https://community-tc.services.mozilla.com/docs/reference/core/hooks) - [service](https://community-tc.services.mozilla.com/hooks)
* Secrets - [docs](https://community-tc.services.mozilla.com/docs/reference/core/secrets) - [service](https://community-tc.services.mozilla.com/secrets)
