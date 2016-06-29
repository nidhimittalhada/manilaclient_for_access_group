# Copyright 2015 Wipro Technologies
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""Interface for access groups."""

from six.moves.urllib import parse

from manilaclient import api_versions
from manilaclient import base
from manilaclient.openstack.common.apiclient import base as common_base

RESOURCES_PATH = '/access_groups'
RESOURCE_PATH = '/access_groups/%s'
RESOURCE_PATH_ACTION = '/access_groups/%s/action'
RESOURCES_NAME = 'access_groups'
RESOURCE_NAME = 'access_group'


class AccessGroup(common_base.Resource):
    """Represents an access group."""

    def __repr__(self):
        return "<AccessGroup: %s>" % self.id

class AccessGroupManager(base.ManagerWithFind):
    """Manage :class:`AccessGroup` resources."""
    resource_class = AccessGroup

    def create(self, name=None, description=None, access_type=None,
        access_level=None):
        """Create an access group.

        :param name: Name of the access_group
        :param description: Description of the access_group
        :param access_type: Access_Type of the access_group
        :param access_level: Access_Level of the access_group
        :rtype: :class:`AccessGroup`
        """
        self._validate_access_type(access_type)
        body = {'name': name,
                'description': description,
                'access_type': access_type,
                'access_level': access_level}
        return self._create(RESOURCES_PATH,
                            {RESOURCE_NAME: body}, RESOURCE_NAME)

    def get(self, access_group):
        """Get an access_group.

        :param access_group: The :class:`AccessGroup` instance or string with ID
               of access_group to delete.
        :rtype: :class:`AccessGroup`
        """
        access_group_id = common_base.getid(access_group)
        print"NMH access_groups.py MANAGER file 1111111333333333",access_group_id
        return self._get(RESOURCE_PATH % access_group_id,
                         RESOURCE_NAME)


    def list(self, detailed=True, search_opts=None, sort_key=None,
             sort_dir=None):
        """Get a list of access_groups.

        :param search_opts: Search options to filter out access_groups.
        :rtype: list of :class:`AccessGroup`
        """
        if search_opts is None:
            search_opts = {}
        
        query_string = self._query_string_helper(search_opts)

        print"NMH 444444444 detailed is",detailed
        if detailed:
            print"i m here 1111"
            path = "/access_groups/detail%s" % (query_string,)
        else:
            print"i m here 222222"
            path = "/access_groups%s" % (query_string,)
        print"NMH 444444444 path is",path

        return self._list(path, RESOURCES_NAME)
    
    
    def _query_string_helper(self, search_opts):
        q_string = parse.urlencode(
            sorted([(k, v) for (k, v) in list(search_opts.items()) if v]))
        if q_string:
            q_string = "?%s" % (q_string,)
        else:
            q_string = ''
        return q_string
    
    def _validate_access_type(self, access_type):
        if access_type not in['ip', 'user', 'cert']:
            raise exceptions.CommandError(
                'Only ip, user, and cert types are supported')

##########
