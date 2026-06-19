# Pydoll maps Flow contracts; the FlowKit extension executes production requests

Pydoll is used for passive CDP Network monitoring of the Flow UI so Omni Flash features can be mapped, sanitized, normalized, and converted into FlowKit contract fixtures. Production agent/script calls should use FlowKit's existing Chrome extension transport for authenticated browser-context execution, after the extension and local API are hardened.

## Consequences

- Do not use Pydoll Fetch interception, request mutation, token replay, or bypass behavior during mapping.
- Do not build a production Pydoll transport before the Omni contracts and extension path have been validated.
- The first concrete deliverable is a FlowKit implementation requirements map: captured endpoints, request/response contracts, model/capability gaps, schema changes, queue/request changes, persistence changes, and tests needed for Omni Flash support.
