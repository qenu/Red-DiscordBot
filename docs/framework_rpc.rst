.. rpc docs

===
RPC
===

V3 comes default with an internal RPC server that may be used to remotely control the bot in various ways.
Cogs must register functions to be exposed to RPC clients.
Each of those functions must only take JSON serializable parameters and must return JSON serializable objects.

To enable the internal RPC server you must start the bot with the ``--rpc`` flag.

********
Examples
********

.. code-block:: Python

    def setup(bot):
        c = Cog()
        bot.add_cog(c)
        bot.register_rpc_handler(c.rpc_method)

*******************************
Interacting with the RPC Server
*******************************

The RPC server opens a websocket bound to port ``6133`` on ``127.0.0.1``.
This is not configurable for security reasons as broad access to this server gives anyone complete control over your bot.
To access the server you must find a library that implements websocket based JSONRPC in the language of your choice.

There are a few built-in RPC methods to note:

* ``GET_METHODS`` - Returns a list of available RPC methods.
* ``GET_METHOD_INFO`` - Will return the docstring for an available RPC method. Useful for finding information about the method's parameters and return values.
* ``GET_TOPIC`` - Returns a list of available RPC message topics.
* ``GET_SUBSCRIPTIONS`` - Returns a list of RPC subscriptions.
* ``SUBSCRIBE`` - Subscribes to an available RPC message topic.
* ``UNSUBSCRIBE`` - Unsubscribes from an RPC message topic.

All RPC methods accept a list of parameters.
The built-in methods above expect their parameters to be in list format.

All cog-based methods expect their parameter list to take one argument, a JSON object, in the following format::

    params = [
        {
            "args": [],  # A list of positional arguments
            "kwargs": {},  # A dictionary of keyword arguments
        }
    ]

    # As an example, here's a call to "get_method_info"
    rpc_call("GET_METHOD_INFO", ["get_methods",])

    # And here's a call to "core__load"
    rpc_call("CORE__LOAD", {"args": [["general", "economy", "downloader"],], "kwargs": {}})

*************
API Reference
*************

Please see the :class:`redbot.core.bot.RedBase` class for details on the RPC handler register and unregister methods.


****************
Core RPC methods 
****************

Below is a list of all RPC methods that are included in Red. Some of them might require you to load a specific cog.

.. important::

    Remember that all RPC methods exposed by Red are not covered by our version guarantees and may break without notice.

Core
----

.. describe:: CORE__UNLOAD

    Unloads cogs with the given names.

    **Request info**

    .. tabs::

        .. tab:: JSON params

            .. list-table::
                :widths: auto
                :header-rows: 1

                * - Field
                  - Type
                  - Description
                * - cog_names
                  - array of strings
                  - array of cog names to unload

        .. tab:: Example payload

            .. sourcecode:: json

                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "CORE__UNLOAD",
                    "params": {
                        "cog_names": ["admin", "downloader"]
                    }
                }

    **Response**

    .. tabs::

        .. tab:: Response fields

            .. list-table::
                :widths: auto
                :header-rows: 1

                * - Field
                  - Type
                  - Description
                * - unloaded_packages
                  - array of strings
                  - array of cog names that were unloaded successfully
                * - failed_packages
                  - array of strings
                  - array of cog names that were not loaded

        .. tab:: Example payload

            .. sourcecode:: json

                {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "result": {
                        "unloaded_packages": ["admin"],
                        "failed_packages": ["downloader"]
                    }
                }


.. describe:: CORE__UNLOAD

    Unloads cogs with the given names.

    **JSON params**

    .. list-table::
        :widths: auto
        :header-rows: 1

        * - Field
          - Type
          - Description
        * - cog_names
          - array of strings
          - array of cog names to unload

    **Response fields**

    .. list-table::
        :widths: auto
        :header-rows: 1

        * - Field
          - Type
          - Description
        * - unloaded_packages
          - array of strings
          - array of cog names that were unloaded successfully
        * - failed_packages
          - array of strings
          - array of cog names that were not loaded

    **Example request payload**

    .. sourcecode:: json

        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "CORE__UNLOAD",
            "params": {
                "cog_names": ["admin", "downloader"]
            }
        }

    **Example response**

    .. sourcecode:: json

        {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "unloaded_packages": ["admin"],
                "failed_packages": ["downloader"]
            }
        }
