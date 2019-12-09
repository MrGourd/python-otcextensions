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
from otcextensions.sdk.ces.v1 import metric as _metric
from otcextensions.sdk.ces.v1 import quota as _quota
from otcextensions.sdk.ces.v1 import alarm as _alarm

from openstack import proxy


class Proxy(proxy.Proxy):

    skip_discovery = True

    # ======== Metrics ========
    def metrics(self, **query):
        """Return a generator of metrics

        :param kwargs query: Optional query parameters to be sent to limit
                              the resources being returned.
        :returns: A generator of metric objects
        :rtype: :class:`~otcextensions.sdk.ces.v1.metric.Metric`
        """
        return self._list(_metric.Metric, **query)

    # ======== Quotas ========
    def quotas(self):
        """Return a generator of quotas

        :returns: A generator of metric objects
        :rtype: :class:`~otcextensions.sdk.ces.v1.quota.Quota`
        """
        return self._list(_quota.Quota)

    # ======== Alarms ========
    def alarms(self):
        """Return a generator of alarms

        :returns: A generator of alarm objects
        :rtype: :class:`~otcextensions.sdk.ces.v1.alarm.Alarm`
        """
        return self._list(_alarm.Alarm)