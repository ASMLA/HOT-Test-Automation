*** Settings ***
Documentation    Generic production-readiness and framework-governance helpers.
Library          Collections
Resource         ../../variables/governance.resource
Resource         logging.resource

*** Keywords ***
Build Production Readiness Criteria
    [Arguments]    ${pass_rate}    ${flaky_rate}    ${documentation_current}=True    ${ci_green}=True    ${secrets_protected}=True
    ${criteria}=    Create Dictionary
    ...    pass_rate=${pass_rate}
    ...    flaky_rate=${flaky_rate}
    ...    documentation_current=${documentation_current}
    ...    ci_green=${ci_green}
    ...    secrets_protected=${secrets_protected}
    RETURN    ${criteria}

Evaluate Production Readiness
    [Arguments]    ${criteria}
    ${pass_rate}=    Convert To Number    ${criteria}[pass_rate]
    ${flaky_rate}=    Convert To Number    ${criteria}[flaky_rate]
    ${minimum}=    Convert To Number    ${DEFAULT_MINIMUM_PASS_RATE}
    ${maximum_flaky}=    Convert To Number    ${DEFAULT_MAXIMUM_FLAKY_RATE}
    ${pass_ok}=    Evaluate    $pass_rate >= $minimum
    ${flaky_ok}=    Evaluate    $flaky_rate <= $maximum_flaky
    ${docs_ok}=    Convert To Boolean    ${criteria}[documentation_current]
    ${ci_ok}=    Convert To Boolean    ${criteria}[ci_green]
    ${secrets_ok}=    Convert To Boolean    ${criteria}[secrets_protected]
    ${ready}=    Evaluate    $pass_ok and $flaky_ok and $docs_ok and $ci_ok and $secrets_ok
    RETURN    ${ready}

Build Governance Metadata
    [Arguments]    ${version}    ${owner}    ${status}
    ${metadata}=    Create Dictionary
    ...    governance_version=${FRAMEWORK_GOVERNANCE_VERSION}
    ...    framework_version=${version}
    ...    owner=${owner}
    ...    status=${status}
    RETURN    ${metadata}

Validate Governance Metadata
    [Arguments]    ${metadata}
    Dictionary Should Contain Key    ${metadata}    governance_version
    Dictionary Should Contain Key    ${metadata}    framework_version
    Dictionary Should Contain Key    ${metadata}    owner
    Dictionary Should Contain Key    ${metadata}    status

Log Governance Decision
    [Arguments]    ${version}    ${status}
    Log Framework Info    framework_version=${version}; governance_status=${status}    governance
