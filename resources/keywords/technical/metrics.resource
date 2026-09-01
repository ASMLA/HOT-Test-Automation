*** Settings ***
Documentation    Generic framework metrics helpers.
Resource         ../../variables/metrics.resource
Resource         logging.resource

*** Keywords ***
Calculate Percentage
    [Arguments]    ${part}    ${total}    ${precision}=${METRIC_DEFAULT_PRECISION}
    ${part_number}=    Convert To Number    ${part}
    ${total_number}=    Convert To Number    ${total}
    ${precision_number}=    Convert To Integer    ${precision}
    IF    ${total_number} == 0
        RETURN    ${METRIC_ZERO}
    END
    ${percentage}=    Evaluate    round(($part_number / $total_number) * 100, $precision_number)
    RETURN    ${percentage}

Calculate Pass Rate
    [Arguments]    ${passed}    ${executed}
    ${rate}=    Calculate Percentage    ${passed}    ${executed}
    Log Framework Debug    pass_rate=${rate}    metrics
    RETURN    ${rate}

Calculate Failure Rate
    [Arguments]    ${failed}    ${executed}
    ${rate}=    Calculate Percentage    ${failed}    ${executed}
    Log Framework Debug    failure_rate=${rate}    metrics
    RETURN    ${rate}

Calculate Flaky Rate
    [Arguments]    ${flaky_tests}    ${executed_tests}
    ${rate}=    Calculate Percentage    ${flaky_tests}    ${executed_tests}
    Log Framework Debug    flaky_rate=${rate}    metrics
    RETURN    ${rate}

Calculate Automation Stability Rate
    [Arguments]    ${stable_tests}    ${executed_tests}
    ${rate}=    Calculate Percentage    ${stable_tests}    ${executed_tests}
    Log Framework Debug    stability_rate=${rate}    metrics
    RETURN    ${rate}

Calculate Defect Detection Rate
    [Arguments]    ${automation_detected_defects}    ${total_detected_defects}
    ${rate}=    Calculate Percentage    ${automation_detected_defects}    ${total_detected_defects}
    Log Framework Debug    defect_detection_rate=${rate}    metrics
    RETURN    ${rate}

Calculate Execution Savings
    [Arguments]    ${manual_minutes}    ${automated_minutes}
    ${saved}=    Evaluate    max(float($manual_minutes) - float($automated_minutes), 0)
    RETURN    ${saved}
