#!/bin/bash

# JSBach Logger - Global logging function for JSBach Router
# Path: /usr/local/bin/jsbach-logger.sh (or sourced from workspace)

# Default configuration
LOG_FILE="/var/log/jsbach/user-actions.log"
LOG_TO_FILE=true

# Function to log actions
# Usage: log_action "MODULE" "ACTION" "DETAILS" "LEVEL"
log_action() {
    local module="${1:-SYSTEM}"
    local action="${2:-UNKNOWN}"
    local details="${3:-}"
    local level="${4:-INFO}"

    # Normalize level to lowercase for logger priority, but keep uppercase for the message
    local priority_level="info"
    case "${level,,}" in
        info)    priority_level="info" ;;
        warning) priority_level="warning" ;;
        error)   priority_level="err" ;;
        *)       priority_level="info" ;;
    esac

    # 1. Log to syslog (facility local0)
    # Format: [JSBACH][MODULE][LEVEL] ACTION - DETAILS
    local log_msg="[JSBACH][$module][$level] $action"
    if [ -n "$details" ]; then
        log_msg="$log_msg - $details"
    fi

    # Execute logger, ensure it doesn't break even if logger fails
    logger -p "local0.$priority_level" "$log_msg" 2>/dev/null || true

    # 2. Log to local file if enabled
    if [ "$LOG_TO_FILE" = true ]; then
        local log_dir
        log_dir=$(dirname "$LOG_FILE")

        # Try to create directory if it doesn't exist
        if [ ! -d "$log_dir" ]; then
            mkdir -p "$log_dir" 2>/dev/null || true
        fi

        # Append to log file if writable
        if [ -w "$log_dir" ] || [ -w "$LOG_FILE" ] || [ ! -e "$LOG_FILE" -a -w "$log_dir" ]; then
            echo "$(date '+%b %d %H:%M:%S') $(hostname) JSBACH: $log_msg" >> "$LOG_FILE" 2>/dev/null || true
        fi
    fi
}

# Export the function so it's available in subshells if sourced
export -f log_action
