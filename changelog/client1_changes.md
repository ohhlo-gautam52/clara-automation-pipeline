## Version v2 Changes

### business_hours
- Old: `{
  "days": [],
  "start": "",
  "end": "",
  "timezone": ""
}`
- New: `{
  "days": [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri"
  ],
  "start": "08:00",
  "end": "18:00",
  "timezone": "CST"
}`
- Reason: Confirmed during onboarding call

### integration_constraints
- Old: `[]`
- New: `[
  "Never create sprinkler jobs in ServiceTrade"
]`
- Reason: Confirmed during onboarding call

