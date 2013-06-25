# REST Mirror

This is a simple AppEngine app that can be used to POST HTTP requests and it will
echo a response with the same Content-Type and body.  It was built to help test 
[HTTPBuilder](http://groovy.codehaus.org/modules/http-builder/).

## A Groovy Example for HTTPBuilder

    @Grab( group='org.codehaus.groovy.modules.http-builder', 
           module='http-builder', version='0.6.0' )

    def builder = new HTTPBuilder("http://restmirror.appspot.com/")
    def result = builder.request(POST, JSON) { req ->
        body = [name: 'bob', title: 'construction worker']

        response.success = {resp, json ->
            println "JSON POST Success: ${resp.statusLine}"
            assert json instanceof net.sf.json.JSONObject
            assert json.name == 'bob'
            return json.name
        }

        response.failure = {resp ->
            println "JSON POST Failed: ${resp.statusLine}"
        }
    }
    assert result == 'bob'

