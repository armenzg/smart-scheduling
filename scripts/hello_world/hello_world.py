#!/usr/bin/env python3
import taskcluster

def main():
    secrets = taskcluster.Secrets(taskcluster.optionsFromEnvironment())
    secret = secrets.get("project/cia/garbage/foo")
    print(secret["secret"])

if __name__ == "__main__":
    main()