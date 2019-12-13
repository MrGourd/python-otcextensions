# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from openstack import exceptions
from openstack import resource


# class MetaDataSpec(resource.Resource):

# Properties
# Number of returned results / alarms
# count = resource.Body('count')
# Indicates pagination marker
# marker = resource.Body('marker')
# Number of total queried results / alarms
# total = resource.Body('total')

class AlarmActionsSpec(resource.Resource):

    # Properties
    # notification list ID
    notificationList = resource.Body('notificationList')
    # Indicates the type of action triggered by an alarm.
    # Value can be notication or autoscaling
    typestring = resource.Body('type')


class ConditionSpec(resource.Resource):

    # Properties
    # indicates the comparison operator
    # values can be <,=,>,>= or <=
    comparison_operator = resource.Body('comparison_operator')
    # Indicates how many consecutive times an alarm has
    # been generated
    count = resource.Body('count', type=int)
    # indicates the data rollup method
    # values: max, min, average, sum, variance
    filterstring = resource.Body('filter')
    # Indicates the interval (in seconds) for checking
    # whether the configured alarm rules are met
    period = resource.Body('period', type=int)
    # Data unit
    unit = resource.Body('unit')
    # Alarm threshold
    value = resource.Body('value')


class DimensionsSpec(resource.Resource):

    # Properties
    #: dimension.name: object type e.g. ECS (instance_id)
    name = resource.Body('name')
    #: dimension.value: object id e.g. ECS ID
    value = resource.Body('value')


class MetricSpec(resource.Resource):

    # Properties
    # List of metric dimensions
    dimensions = resource.Body('dimensions', type=list,
                               list_type=DimensionsSpec)
    # Metric name, such as cpu_util in ECS metrics
    metric_name = resource.Body('metric_name')
    # Metric Namespace
    namespace = resource.Body('namespace')


class Alarm(resource.Resource):

    resources_key = 'metric_alarms'
    base_path = '/alarms'

    # capabilities
    allow_commit = True
    allow_create = True
    allow_fetch = True
    allow_delete = True
    allow_list = True

    _query_mapping = resource.QueryParameters(
        'limit', 'order', 'start'
    )

    # Properties
    # Indicates the action triggered by clearing an alarm
    alarm_actions = resource.Body('alarm_actions', type=AlarmActionsSpec)
    # Indicates whether an action will be triggered by an alarm
    # True: action will be triggered
    # False: action will not be triggered
    alarm_action_enabled = resource.Body('alarm_action_enabled', type=bool)
    # Description of the alarm
    alarm_description = resource.Body('alarm_description')
    # Alarm is enabled (True) or disabled (False)
    alarm_enabled = resource.Body('alarm_enabled', type=bool)
    # alarm rule ID
    alarm_id = resource.Body('alarm_id', alternate_id=True)
    # alarm severity
    # values: 1: critical, 2: major, 3: minor, 4: informational alarm
    alarm_level = resource.Body('alarm_level', type=int)
    # Name of the alarm
    alarm_name = resource.Body('alarm_name')
    # Alarm status
    # ok: alarm status is normal
    # alarm: an alarm is generated
    # insufficient_data: required data is insufficient
    alarm_state = resource.Body('alarm_state')
    # Describes alarm triggering condititon
    condititon = resource.Body('condition', type=ConditionSpec)
    # Specification of specific alarm
    metric = resource.Body('metric', type=MetricSpec)
    # Time when alarm status changed
    # UNIX timestamp in ms
    update_time = resource.Body('update_time')

    def _translate_response(self, response, has_body=None, error_message=None):
        """Given a KSA response, inflate this instance with its data

        DELETE operations don't return a body, so only try to work
        with a body when has_body is True.

        This method updates attributes that correspond to headers
        and body on this instance and clears the dirty set.
        """
        if has_body is None:
            has_body = self.has_body
        exceptions.raise_from_response(response, error_message=error_message)
        if has_body:
            try:
                body = response.json()
                if self.resources_key and self.resources_key in body:
                    body = body[self.resources_key][0]
                body_attrs = self._consume_body_attrs(body)
                self._body.attributes.update(body_attrs)
                self._body.clean()

            except ValueError:
                # Server returned not parse-able response (202, 204, etc)
                # Do simply nothing
                pass

        headers = self._consume_header_attrs(response.headers)
        self._header.attributes.update(headers)
        self._header.clean()
        self._update_location()
        dict.update(self, self.to_dict())
