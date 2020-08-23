# Set up development environment

## Install Python 3

Get [Python 3 here](https://www.python.org/).

## Install OpenJDK

Install Java JDK (I recommend **OpenJDK 11** from [AdoptOpenJDK](https://adoptopenjdk.net/)) - this is needed to run the 
Datastore or Firestore emulator (via Cloud SDK).

## Install PyCharm

Install PyCharm: [https://www.jetbrains.com/pycharm/](https://www.jetbrains.com/pycharm/). Community edition would do, 
but if you want, you can buy yourself the Professional edition.

## Install Cloud SDK

Install [Cloud SDK](https://cloud.google.com/sdk/docs/quickstarts).

## Install Cloud SDK components

Make sure you have the following Cloud SDK components installed:

- Cloud SDK Core Libraries (core)
- gcloud app Python Extensions (app-engine-python)
- gcloud app Python Extensions - Extra Libraries (app-engine-python-extras)
- gcloud Beta Commands (beta)

If you'll use Datastore or Firestore, you'll need to install one of these (or both) components too:

- Cloud Datastore Emulator (cloud-datastore-emulator)
- Cloud Firestore Emulator (cloud-firestore-emulator)

### Cloud SDK components: Installation process

Firstly, check which of these components you have already installed:

    gcloud components list

At least one or two of them should already be installed. For the others, install them using this command:

    gcloud components install <component-name>

For example, if you want to install the Datastore Emulator, use this command:

    gcloud components install cloud-datastore-emulator

Also, make sure that your already installed components are up-to-date:

    gcloud components update

If you need more instructions, check here: ([Cloud SDK components documentation](https://cloud.google.com/sdk/docs/components))

