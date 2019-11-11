# See the data in Datastore visually on localhost

If you'd like to see what data are stored in the localhost Datastore emulator, install 
[Datastore Viewer](https://github.com/gumo-py/datastore-viewer):

    pip install datastore-viewer

Then you can run the Datastore Viewer using this command (note that Datastore emulator needs to be running!):

    # mac & linux:
    export DATASTORE_EMULATOR_HOST=localhost:8001 && datastore-viewer
    
    # windows
    set DATASTORE_EMULATOR_HOST=localhost:8001 && datastore-viewer

Datastore Viewer will run on [http://127.0.0.1:8082/](http://127.0.0.1:8082/). Enter `test` as the project name and 
you'll see the data in your Datastore.

## Links:

- [Index](/README.md#documentation)
