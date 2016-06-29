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
from manilaclient.common import constants
from manilaclient.v2 import access_groups as ag

RESOURCES_PATH = '/access_groups_entries'
RESOURCE_PATH = '/access_groups_entries/%s'
RESOURCES_NAME = 'access_group_entries'
RESOURCE_NAME = 'access_group_entry'

class AccessGroupEntry(common_base.Resource):
    """Represents an access group entry."""

    def __repr__(self):
        return "<AccessGroupEntry: %s>" % self.id
    
    def delete(self):
        """Delete this access_group_entry."""
        self.manager.delete(self)
    
class AccessGroupEntriesManager(base.ManagerWithFind):
    """Manage :class:`AccessGroupEntry` resources."""
    resource_class = AccessGroupEntry

    def create(self, access_to=None, access_group_id=None):
        """Create an access group entry.

        :param access_to: Value that defines access
        :param access_group_id: ID of access_group
        :rtype: :class:`AccessGroupEntry`
        """
        body = {'access_to': access_to,
                'access_group_id': access_group_id}
        return self._create(RESOURCES_PATH,
                            {RESOURCE_NAME: body}, RESOURCE_NAME)

    def get(self, access_group_entry):
        """Get an access_group_entry.

        :param access_group_entry: The :class:`AccessGroupEntry` instance or string with ID
               of access_group_entry.
        :rtype: :class:`AccessGroupEntry`
        """
        access_group_entry_id = common_base.getid(access_group_entry)
        print"NMH access_groups_entries.py MANAGER file 111111133333 access_group_entry_id is",access_group_entry_id
        return self._get(RESOURCE_PATH % access_group_entry_id,
                         RESOURCE_NAME)


    def list(self, detailed=True, search_opts=None, sort_key=None,
             sort_dir=None):
        """Get a list of access_group_entries.

        :param search_opts: Search options to filter out access_group_entries.
        :rtype: list of :class:`AccessGroupEntry`
        """
        print"NMH 444444444 detailed is",detailed
        print"NMH 44444 search_opts is",search_opts

        if search_opts is None:
            search_opts = {}
         
        if sort_key is not None:
            if sort_key.strip().lower() in constants.ACCESS_GROUP_ENTRY_SORT_KEY_VALUES:
                search_opts['sort_key'] = sort_key
            else:
                raise ValueError(
                    'sort_key must be one of the following: %s.'
                    % ', '.join(constants.ACCESS_GROUP_ENTRY_SORT_KEY_VALUES))

        if sort_dir is not None:
            if sort_dir.strip().lower() in constants.SORT_DIR_VALUES:
                search_opts['sort_dir'] = sort_dir
            else:
                raise ValueError(
                    'sort_dir must be one of the following: %s.'
                    % ', '.join(constants.SORT_DIR_VALUES))

        if search_opts:
            query_string = self._query_string_helper(search_opts)
        
        print"NMH 44444 query_string is",query_string
        
        if detailed:
            path = RESOURCES_PATH + "/detail%s" % (query_string,)
        else:
            path = RESOURCES_PATH + "%s" % (query_string,)

        print"NMH 444444444 path is",path
        return self._list(path, RESOURCES_NAME)
    
    def delete(self, access_group_entry):
        """Delete an access group entry.

        :param access_group_entry: The :class:`AccessGroupEntry` to delete.
        """
        self._delete(RESOURCE_PATH % common_base.getid(access_group_entry))

    def _query_string_helper(self, search_opts):
        q_string = parse.urlencode(
            sorted([(k, v) for (k, v) in list(search_opts.items()) if v]))
        if q_string:
            q_string = "?%s" % (q_string,)
        else:
            q_string = ''
        return q_string
    
    def _validate_access(self, access_type, access):
        if access_type == 'ip':
            self._validate_ip_range(access)
        elif access_type == 'user':
            self._validate_username(access)
        elif access_type == 'cert':
            # 'access' is used as the certificate's CN (common name)
            # to which access is allowed or denied by the backend.
            # The standard allows for just about any string in the
            # common name. The meaning of a string depends on its
            # interpretation and is limited to 64 characters.
            self._validate_common_name(access.strip())
        else:
            raise exceptions.CommandError(
                'Only ip, user, and cert types are supported')

    @staticmethod
    def _validate_username(access):
        valid_username_re = '[\w\.\-_\`;\'\{\}\[\]\\\\]{4,32}$'
        username = access
        if not re.match(valid_username_re, username):
            exc_str = ('Invalid user or group name. Must be 4-32 characters '
                       'and consist of alphanumeric characters and '
                       'special characters ]{.-_\'`;}[\\')
            raise exceptions.CommandError(exc_str)

    @staticmethod
    def _validate_ip_range(ip_range):
        ip_range = ip_range.split('/')
        exc_str = ('Supported ip format examples:\n'
                   '\t10.0.0.2, 10.0.0.0/24')
        if len(ip_range) > 2:
            raise exceptions.CommandError(exc_str)
        if len(ip_range) == 2:
            try:
                prefix = int(ip_range[1])
                if prefix < 0 or prefix > 32:
                    raise ValueError()
            except ValueError:
                msg = 'IP prefix should be in range from 0 to 32'
                raise exceptions.CommandError(msg)
        ip_range = ip_range[0].split('.')
        if len(ip_range) != 4:
            raise exceptions.CommandError(exc_str)
        for item in ip_range:
            try:
                if 0 <= int(item) <= 255:
                    continue
                raise ValueError()
            except ValueError:
                raise exceptions.CommandError(exc_str)

