# -*- coding: utf-8 -*-

import requests
import simplejson as json

class _api():
    def __init__(self, apiurl='http://localhost/api', username=None, password=None, token=None):
        self.apiurl = apiurl
        self.username = username
        self.password = password
        self.token = token

        self.headers = {}
        self.headers['Content-Type'] = 'application/json'
        self.headers['Accept'] = "application/json; indent=4"
        if token:
            self.headers['Authorization'] = token
        self.auth=None
        if username and password:
            self.auth = (username,password)

    def endpoint(self, resource):
        return '{}/{}'.format(self.apiurl,resource)

class operators(_api):

    def listOperators(self):
        return requests.get(self.endpoint('operators'), auth=self.auth, headers=self.headers) 

    def findOperator(self, opName):
        url = '{}?where={{"name": "{}"}}'.format(self.endpoint('operators'), opName)
        return requests.get(url, auth=self.auth, headers=self.headers) 

    def createOperator(self, data):
        return requests.post(self.endpoint('operators'), json.dumps(data), auth=self.auth, headers=self.headers) 

    def updateOperator(self, opID, etag, data):
        headers = self.headers
        headers['If-Match'] = etag
        return requests.patch(self.endpoint('operators/{}'.format(opID)), json.dumps(data), auth=self.auth, headers=self.headers)

    def deleteOperator(self, opID, etag):
        headers = self.headers
        headers['If-Match'] = etag
        return requests.delete(self.endpoint('operators/{}'.format(opID)), auth=self.auth, headers=headers)

class secrets(_api):

    def listSecretsStores(self,where=None):
        url = "{}?sort=category,name".format(self.endpoint('secrets'))
        if where:
            url = '{}&where={}'.format(url,where)
        return requests.get(url, auth=self.auth, headers=self.headers) 

    def findSecretsStore(self, store):
        url = '{}?where={{"name": "{}"}}'.format(self.endpoint('secrets'), store)
        return requests.get(url, auth=self.auth, headers=self.headers)

    def createSecretsStore(self, data):
        return requests.post(self.endpoint('secrets'), json.dumps(data), auth=self.auth, headers=self.headers)

    def updateSecretsStore(self, passwordID, etag, data):
        headers = self.headers
        headers['If-Match'] = etag
        return requests.patch(self.endpoint('secrets/{}'.format(passwordID)), json.dumps(data), auth=self.auth, headers=headers)

    def deleteSecretsStore(self, passwordID, etag):
        headers = self.headers
        headers['If-Match'] = etag
        return requests.delete(self.endpoint('secrets/{}'.format(passwordID)), auth=self.auth, headers=headers)

