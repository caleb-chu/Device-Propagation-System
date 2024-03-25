**Distributed System Simulation**

The input file consists of lines of text, each describing a specific aspect of the simulation:

LENGTH: Specifies the length of the simulation in milliseconds.

DEVICE: Establishes the existence of a device with a unique ID.

PROPAGATE: Describes a rule for propagating alerts or cancellations between devices.

ALERT: Specifies when a device raises an alert with a given description.

CANCEL: Specifies when a device cancels an alert with a given description.

Blank lines and comments (lines starting with #) for readability.

**Output Format**

The program outputs events during the simulation:

Device receives an alert: @<time>: #<receiver_device> RECEIVED ALERT FROM #<sender_device>: <alert_description>

Device sends or propagates an alert: @<time>: #<sender_device> SENT ALERT TO #<receiver_device>: <alert_description>

Device receives a cancellation: @<time>: #<receiver_device> RECEIVED CANCELLATION FROM #<sender_device>: <cancellation_description>

Device sends or propagates a cancellation: @<time>: #<sender_device> SENT CANCELLATION TO #<receiver_device>: <cancellation_description>

Simulation ends: @<end_time>: END

The simulation progresses according to the specified times in milliseconds.

Events scheduled at the same time can occur in any order.

The simulation ends at the specified time, regardless of ongoing propagation.

Refer to sample_input.txt and sample_output.txt for an example scenario and its corresponding output.
